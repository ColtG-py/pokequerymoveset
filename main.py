import pokepy
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from PyInquirer import prompt

console = Console()

'''
red-blue
gold-silver
ruby-sapphire
platinum
'''

'''================================================================================================
promptResponse

@param question - question displayed on console

@return response from user
================================================================================================'''
def promptResponse(question) -> str:
    question = prompt(
        {
            "type": "input",
            "name": "response",
            "message": question
        }
    )
    return question.get("response")

'''================================================================================================
promptGeneration

@param question - question displayed on console

@return yes or no response from user
================================================================================================'''
def promptGeneration(question) -> str:
    question = prompt(
        {
            "type": "list",
            "name": "response",
            "message": question,
            "choices": ["red-blue", "gold-silver", "ruby-sapphire", "platinum"]
        }
    )
    return question.get("response")

def main(pokename: str):

    client = pokepy.V2Client()

    target_pokemon = pokename
    target_generation = promptGeneration("What generation is it from?")

    pokemon = client.get_pokemon(target_pokemon)
    print(pokemon)
    print(dir(pokemon))
    moves = pokemon.moves

    filtered_moves = [
        move
        for move in moves
        if any(detail.version_group.name == target_generation for detail in move.version_group_details)
    ]

    genMoves = []
    tmMoves = []
    for move in filtered_moves:
        move_name = move.move.name
        level_learned = move.version_group_details[0].level_learned_at
        if (level_learned != 0):
            move_details = client.get_move(move.move.name)
            move_name = move_details.name
            power = move_details.power
            priority = move_details.priority
            pp = move_details.pp
            acc = move_details.accuracy
            dtype = move_details.damage_class.name
            ttype = move_details.type.name
            genMoves.append((level_learned, move_name, power, pp, acc, priority, dtype, ttype))
        else:
            move_details = client.get_move(move.move.name)
            move_name = move_details.name
            power = move_details.power
            priority = move_details.priority
            pp = move_details.pp
            acc = move_details.accuracy
            dtype = move_details.damage_class.name
            ttype = move_details.type.name
            tmMoves.append((level_learned, move_name, power, pp, acc, priority, dtype, ttype))

    # # Sort the moves based on level learned in ascending order
    genMoves.sort(key=lambda move: move[0])

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("LEVEL LEARNED", width=5)
    table.add_column("MOVE NAME", style="dim", width=20)
    table.add_column("POWER", width=5)
    table.add_column("PP", width=3)
    table.add_column("ACC", width=3)
    table.add_column("PRIO", width=4)
    table.add_column("DMG CLASS", width=10)
    table.add_column("DMG TYPE", width=10)

    for move in genMoves:
        table.add_row(str(move[0]), str(move[1]), str(move[2]), str(move[3]), str(move[4]), str(move[5]), str(move[6]), str(move[7]))

    print(table)
    
if __name__=='__main__':
    typer.run(main)
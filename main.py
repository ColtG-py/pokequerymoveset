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
    moves = pokemon.moves

    filtered_moves = [
        move
        for move in moves
        if any(detail.version_group.name == target_generation for detail in move.version_group_details)
    ]

    genMoves = []
    for move in filtered_moves:
        move_name = move.move.name
        level_learned = move.version_group_details[0].level_learned_at
        if (level_learned != 0):
            genMoves.append((move_name,level_learned))
            
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("MOVE NAME", style="dim", width=60)
    table.add_column("LEVEL LEARNED", width=5)

    for move in genMoves:
        table.add_row(str(move[0]), str(move[1]))

    print(table)
    
if __name__=='__main__':
    typer.run(main)
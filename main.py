import pokepy

client = pokepy.V2Client()

target_pokemon = "gible"
target_generation = "platinum"

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
        genMoves.append(f"{move_name} : {level_learned}")
        
for move in genMoves:
    print(move)
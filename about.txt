FR - field with read
FP - full private field
FL - link field
P - property


Experience:
    FR exp: int <- add_exp(exp), lost_exp(exp)
    FP exp_road: list<int>
    FR max_level: int
    P level: int
    P for_next_level: int

Voice:
    FP messages: dict <- speak(key, default), change_message(key, value)

Health:
    FR health: float <- accept_attack(attack), accept_heal(heal), refresh_health(), resurrect()
    FR max_health: float

BaseAnimal:
    FR name: string <- rename(new)
    FL health: Health
    FR attack: int <- make_damage(another)
    FR age: int
    FR color: string
    FR abilities: list<Ability>
    FL experience: Experience
    P dead: bool

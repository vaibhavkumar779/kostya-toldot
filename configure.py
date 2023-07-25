import json

default_config = dict(
    last_parsed=None,
    force_parse_all=False,
    parse_every=24,
    every_what='hours'
)


def read_config():
    with open('config.json') as file:
        config = json.load(file)
        return config


def save_config(config: dict):
    with open('config.json', 'w') as file:
        json.dump(config, file)


def ask_yes_no(question, cur_value=None):
    cur_value_txt = f' (current value: {cur_value})' if cur_value is not None else ''
    print(question+cur_value_txt)
    while True:
        answer = input('\nAnswer [Y/n]: ')
        if not answer and cur_value is not None:
            return cur_value
        answer = answer.lower().strip()
        if answer in ['yes', 'y']:
            return True
        elif answer in ['no', 'n']:
            return False
        print('Wrong value')


def ask_for_choice(question, choices, cur_value=None):
    cur_value_txt = f' (current value: {cur_value})' if cur_value is not None else ''
    print(question+cur_value_txt)
    for i, choice in enumerate(choices):
        print(f'[{i+1}] {choice}')

    while True:
        try:
            answer = input('\nAnswer: ')
            if not answer and cur_value is not None:
                return cur_value
            answer = int(answer.strip())
        except ValueError:
            print('Wrong value')
            continue
        if answer in range(1, len(choices)+2):
            return choices[answer-1]
        print('Wrong value')


def ask_for_value(question, value_type, cur_value=None):
    cur_value_txt = f' (current value: {cur_value})' if cur_value is not None else ''
    print(question+cur_value_txt)

    while True:
        try:
            answer = input(f'\nAnswer ({value_type.__name__}): ')
            if not answer and cur_value is not None:
                return cur_value
            answer = value_type(answer.strip())
            return answer
        except ValueError:
            print('Wrong value')


if __name__ == '__main__':
    time_measure = ['seconds', 'minutes', 'hours']
    config = read_config()

    config['force_parse_all'] = ask_yes_no(f'Force parse all the site, not only new data.',
                                           cur_value=config["force_parse_all"])
    config['parse_every'] = ask_for_value(f'Parse every...', int, cur_value=config["parse_every"])
    config['every_what'] = ask_for_choice(f'Parse every what...', time_measure,
                                          cur_value=config["every_what"])

    summary = f"Check settings! Is it right?\nParse every {config['parse_every']} {config['every_what']}!" \
              f"\nForce parsing: {config['force_parse_all']}"

    if ask_yes_no(summary):
        save_config(config)
        print('Config updated!')

from pipa.pipa import Pipa


class Main:
    def run() -> None:
        print('Deploying template...')
        Pipa.init_template('my_project')
        print('Deploying venv...')
        Pipa.init_venv()
        print('Deployed settings...')
        Pipa.init_settings()
        print('Installing basic packages...')
        Pipa.init_requirements()
        print('Initializing git...')
        Pipa.init_git()
        print('Done.')


if __name__ == '__main__':
    Main.run()
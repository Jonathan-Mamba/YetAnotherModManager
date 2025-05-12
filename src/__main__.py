from src import view, model


def main():
    view.CommandLineView(model.LinuxModel()).run()

if __name__ == "__main__":
    main()
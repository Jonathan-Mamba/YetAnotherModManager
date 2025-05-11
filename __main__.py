import view
import model



def main():
    view.CommandLineView(model.LinuxModel()).run()

if __name__ == "__main__":
    main()
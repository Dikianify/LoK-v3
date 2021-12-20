from app import App

def main(app):
    while True:
        app.update()


if __name__ == '__main__':
    app = App()
    main(app)
    
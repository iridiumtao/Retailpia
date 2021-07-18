import src.event_manager as event_manager
import src.model as model
import src.view as view
import src.controller as controller

def run():
    ev_mgr = event_manager.EventManager()
    game_model = model.GameEngine(ev_mgr)
    keyboard = controller.Keyboard(ev_mgr, game_model)
    graphics = view.GraphicalView(ev_mgr, game_model)
    game_model.run()

if __name__ == '__main__':
    run()
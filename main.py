# THIS FILE HOLDS THE MAIN FUNCTIONS THAT INTERACT WITH OUR CONTROLLERS TO DISPLAY THE DATA
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controller import Controller
from views import View

class App:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:admin@localhost:3306/oc_p5")
        self.session = Session(self.engine)
        self.controller = Controller(session=self.session)
        self.controller.add_categories_to_bdd(categories=self.controller.generate_categories(["sandwichs",
                                                                                              "bonbons",
                                                                                              "jambons",
                                                                                              "chips"]))
        self.view = View(session=self.session, controller=self.controller)








app = App()

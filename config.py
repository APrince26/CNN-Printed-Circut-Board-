class Config:
    def __init__(self) -> None:
        self.params = {
            "max_components": 100,
            "num_designs": 5000,
            "component_ds": 8,
            "pin_ds": 2,
            "same_design_size": True,
            "random_changes": False,
            "just_connections": True,
            "connection_color": "red",
            "background_color": "white",
            "make_png_images": True,
            "batch_size": 32,
            "epochs": 25,
            "image_size" : (167, 167)



        }

    def get_make_png_images(self):
        return self.params["make_png_images"]

    def get_batch_size(self):
        return self.params["batch_size"]

    def get_epochs(self):
        return self.params["epochs"]

    def image_size(self):
        return self.params["image_size"]

    def get_max_components(self) -> int:
        return self.params["max_components"]

    def get_num_designs(self) -> int:
        return self.params["num_designs"]

    def get_component_ds(self) -> int:
        return self.params["component_ds"]

    def get_pin_ds(self) -> int:
        return self.params["pin_ds"]

    def get_same_design_size(self) -> bool:
        return self.params["same_design_size"]

    def get_random_changes(self) -> bool:
        return self.params["random_changes"]
    def get_just_connections(self) -> bool:
        return self.params["just_connections"]
    def get_connection_color(self) -> str:
        return self.params["connection_color"]
    def get_background_color(self) -> str:
        return self.params["background_color"]

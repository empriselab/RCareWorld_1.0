import pyrcareworld.attributes as attr

class SpongeAttr(attr.BaseAttr):
    """
    Sponge attribute class to interact with the sponge in the Unity environment.
    """

    def __init__(self, env, id: int, data: dict = {}, buffer: int = 5):
        """
        Initialize the SpongeAttr.

        :param env: Environment object.
        :param id: ID of the object.
        :param data: Optional initial data.
        :param buffer: Number of frames to buffer. Increase if there are 0.0 values being put in between expected non-0 values, or generally, if your unity simulation frame rate is too low.
        """
        self.NUM_ZEROS_TO_RESET = buffer
        self.LAST_NONZERO = [0.0]
        self.NUM_ZERO_CURRENTLY = 0

        super().__init__(env, id, data)

    def parse_message(self, data: dict):
        """
        Parse messages. This function is called by an internal function.

        data['paint_proportion']: Proportion of paint.
        data['forces']: A list of force values.
        """
        super().parse_message(data)
        self.data.update(data)

    def GetPaintProportion(self):
        """
        Get the proportion of the paint on the avatar.
        """
        return self.data.get("paint_proportion", 0.0)

    def GetEffectiveForceProportion(self):
        """
        Get the proportion of effective forces (force within 2 to 12 range).
        """
        return self.data.get("effective_force_proportion", 0.0)

    def GetForce(self) -> list:
        """
        Get the average force magnitude on the sponge from the previous step. For code scalability purposes, is a list with one value.
        """

        # Code to put a few frames' buffer to stabilize reading.
        reading = self.data.get("real_time_force", [0.0]) 

        if reading[0] == 0.0:
            self.NUM_ZERO_CURRENTLY += 1
        else:
            self.LAST_NONZERO = reading
            self.NUM_ZERO_CURRENTLY = 0

        if self.NUM_ZERO_CURRENTLY >= self.NUM_ZEROS_TO_RESET:
            self.LAST_NONZERO = [0.0]

        return self.LAST_NONZERO

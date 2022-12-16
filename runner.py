import logging

from policies import Policies, get_policy


class Runner:
    def __init__(self, list_of_args):
        self.method = None
        self.args = None

        try:
            self.method = Policies(list_of_args[0])  # validating the method
        except ValueError:
            logging.warning(
                f"invalid policy {list_of_args[0]}, the following policies are available {[e.value for e in Policies]}"
            )

        if len(list_of_args) > 1:
            self.args = list_of_args[1:]
        else:
            logging.info("no arguments besides policy")

    def run(self):
        if self.method is not None:
            chosen_policy = get_policy(policy_input=self.method)
            chosen_policy.run(args=self.args)

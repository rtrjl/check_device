import ncs
from nso_live_status import run_live_status
from distutils.version import LooseVersion
from ncs.dp import Action

CHECK_OK = "OK"
CHECK_NOK = "NOK"
CHECK_ERROR = "ERROR"


class CheckVersion(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info(f"Action CheckVersion , device : {input.device} target version : {input.target_version}")
        command = "show version"
        root = ncs.maagic.get_root(trans)

        show_version = run_live_status(root, input.device, command)

        target_version = LooseVersion(input.target_version)
        if show_version.has_structured_output:
            current_version = LooseVersion(show_version.structured_output["software_version"])
            if current_version == target_version:
                output.check_status = CHECK_OK
                output.check_message = f"[check_version] Current version {current_version} match the target version {target_version} on the device {input.device}"
            else:
                output.check_status = CHECK_NOK
                output.check_message = f"[check_version] Current version {current_version} doesn't match the target version {target_version} on the device {input.device}"
        else:
            output.check_status = CHECK_ERROR
            output.check_message = f"[check_version] ERROR unable to retrieve structured output from {input.device} with the command {command}"
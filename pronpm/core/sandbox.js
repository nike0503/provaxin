import child_process from 'child_process';
import config from './config.js';

const PRONPM_CORE_PATH = `${config.PRONPM_PATH}/core`;
const SANDBOX_OUTPUT_PATH = `${PRONPM_CORE_PATH}/output/`;
const SANDBOX_DUMP_FILE = `${SANDBOX_OUTPUT_PATH}sandbox_dump.json`;

export default async function RunInSandbox(file) {
    console.log("  Execution in sandbox started.");
    return await new Promise((resolve, reject) => {
        const {stdout, stderr} = child_process.exec(`node jailme.js ${file} -s ${SANDBOX_OUTPUT_PATH} -o ${SANDBOX_DUMP_FILE} -t 2000 --down`, {
            cwd: config.SANDBOX_PATH,
        }, () => {
            console.log("  Execution in sandbox completed.");
            resolve(SANDBOX_DUMP_FILE);
        });
    });
}

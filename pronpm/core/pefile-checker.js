import child_process from 'child_process';
import config from './config.js';

const PRONPM_CORE_PATH = `${config.PRONPM_PATH}/core`;
const PEFILE_MODEL_PATH = `${config.PRONPM_PATH}/pefile-model`;
const SANDBOX_OUTPUT_PATH = `${PRONPM_CORE_PATH}/output/`;
const PE_FEATURES_FILE = `${SANDBOX_OUTPUT_PATH}eval_features.csv`;

async function ExtractFeatures(files) {
    console.log("    Extracting features from PE files.");
    const filesString = files.join(' ');
    return await new Promise((resolve, reject) => {
        const {stdout, stderr} = child_process.exec(`python pronpm_extractor.py ${PE_FEATURES_FILE} ${filesString}`, {
            cwd: PEFILE_MODEL_PATH,
        }, () => {
            console.log("    Feature extraction completed.");
            resolve(PE_FEATURES_FILE);
        });
    });
}

async function RunModel(featuresFile) {
    console.log("    Running ML analysis on extracted features.");
    return await new Promise((resolve, reject) => {
        const {stdout, stderr} = child_process.exec(`python pronpm_model.py ${featuresFile}`, {
            cwd: PEFILE_MODEL_PATH,
        },  (err, stdout, stderr) => {
            console.log("    ML analysis completed.");
            resolve(stdout);
        });
    });
}

export default async function CheckFiles(files) {
    const fullPaths = files.map(file => SANDBOX_OUTPUT_PATH+file);
    const featuresFile = await ExtractFeatures(fullPaths);
    const output = await RunModel(featuresFile);
    const isAnyFileMalicious = output.includes("1");
    return isAnyFileMalicious;
}

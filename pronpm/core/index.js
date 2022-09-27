import path from 'path';

import RunInSandbox from "./sandbox.js";
import AnalyzeDump  from "./dump-analyzer.js";

const fileName = process.argv[2];
const absoluteFilePath = path.resolve(fileName);
console.log("Checking if the package is a malware...")

const sandboxDump = await RunInSandbox(absoluteFilePath);
const isMalware = await AnalyzeDump(sandboxDump);

if (isMalware) {
    console.log("The package is a malware");
} else {
    console.log("The package is not a malware");
}

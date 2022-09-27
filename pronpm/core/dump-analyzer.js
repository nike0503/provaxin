import fs from 'fs';
import CheckURL from './url-checker.js';
import CheckFiles from './pefile-checker.js';

export default async function AnalyzeDump(dumpFile) {
    const dump = JSON.parse(fs.readFileSync(dumpFile, 'utf-8'));
    
    let isMalware = false;
    
    const urls = dump["_wscript_urls"];
    const numUrls = urls.length;
    console.log("  HTTP request URLs analysis started.");
    if (numUrls == 0) {
        console.log("    No HTTP URLs to analyse.");
    } else {
        console.log(`    Analyzing ${numUrls} URLs.`);
        let totalScore = 0;
        for (let i = 0; i < numUrls; i++) {
            let score = await CheckURL(urls[i]['url']);
            if (score > 85) {
                console.log("    Extremely high risk URL found: ", urls[i]['url']);
                isMalware = true;
                break;
            } else {
                totalScore += score;
            }
        }
        if( totalScore >= 70*numUrls && numUrls > 2) {
            console.log("    Multiple risky URLs found.");
            isMalware = true;
        }
        if (!isMalware) {
            console.log("    All URLs are safe.");
        }
    }
    console.log("  HTTP request URLs analysis complete.");
    if (isMalware) return true;
    
    const savedFiles = dump["_wscript_saved_files"];
    console.log("  Downloaded files analysis started.");
    let execFiles = [];
    for (let key in savedFiles) {
        execFiles.push(key);
    }
    if (execFiles.length != 0) {
        console.log(`    Analyzing ${execFiles.length} downloaded files.`);
        const anyFileIsMalware = await CheckFiles(execFiles);
        if (anyFileIsMalware) {
            console.log("    Malware file found");
            isMalware = true;
        } else {
            console.log("    All downloaded files are safe.");
        }
    } else {
        console.log("    No downloaded files to analyse.");
    }
    console.log("  Downloaded files analysis completed.");

    // More types of analyses can be added here.

    return isMalware;
}

export function printEvals(dumpFile) {
    const dump = JSON.parse(fs.readFileSync(dumpFile, 'utf-8'));
    const evalCalls = dump["_data"]["eval_calls"];
    console.log(dumpFile);
    console.log(evalCalls);
}

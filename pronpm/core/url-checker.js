import fetch from "node-fetch";
import config from "./config.js";

const SAFE_BROWSING_API_URL = `https://safebrowsing.googleapis.com/v4/threatMatches:find?key=${config.SAFE_BROWSING_API_KEY}`
const IP_QUALITY_SCORE_API_URL = `https://ipqualityscore.com/api/json/url/${config.IP_QUALITY_SCORE_API_KEY}`;

/*
 * Not using Google Safe Browsing API for now because
 * upon testing, it didn't classify those URLs as 
 * malicious which were found in actual malware, whereas
 * IPQualityScore API classified them as malicious.
 * 
 * So this function is just for reference.
*/
async function GoogleSafeBrowsingAPIFind(url) {
    const response = await fetch(SAFE_BROWSING_API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({
            client: {
                clientId: "provaxin",
                clientVersion: "1.0.0",
            },
            threatInfo: {
                threatTypes: ["MALWARE","SOCIAL_ENGINEERING","UNWANTED_SOFTWARE","MALICIOUS_BINARY"],
                platformTypes: ["ANY_PLATFORM"],
                threatEntryTypes: ["URL"],
                threatEntries: {"url": url},
            },
        }),
    });
    const data = await response.json();
    return data;
}


async function IPQualityScoreCheck(url) {
    const response = await fetch(`${IP_QUALITY_SCORE_API_URL}/${encodeURIComponent(url)}`);
    const data = await response.json();
    if(data['success']) {
        return data['risk_score'];
    }
    return 0;
}

export default async function CheckURL(url) {
    // return await GoogleSafeBrowsingAPIFind(url); // Not using, for reasons mentioned above 
    return await IPQualityScoreCheck(url);
}

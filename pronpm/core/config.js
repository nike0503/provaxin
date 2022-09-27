/*
    IP_QUALITY_SCORE_API_KEY:   I have provided my key, but it has a limit of 
                                5000 API calls per month. We have already used
                                ~200. Ideally, a production-use key must be used here.

    PRONPM_PATH:                The path where the pronpm folder is. Ideally, this will
                                be known when the propnpm software package is installed.
                                However, here we need to explicitly provide it.
                                An absolute path needs to be provided.

    SANDBOX_PATH:               Our tool uses malware-jail as a dependency. It can be
                                cloned from https://github.com/HynekPetrak/malware-jail
                                We need the path of a clone of this dependency in order
                                to run the sandbox.
                                Again, ideally when we install the pronpm package, this path
                                would be known, but here we need to explicitly provide it.
                                An absolute path needs to be provided.
*/


// Please ensure that there are no trailing slashes in the paths

export default {
    IP_QUALITY_SCORE_API_KEY: "FlUuJ15OUfwAL5lz1CQWmZDhQkpGWVG2",
    
    PRONPM_PATH: "/mnt/mewis/Academics/malware_analyis_CS658A/provaxin/pronpm",
    SANDBOX_PATH: "/mnt/mewis/Academics/malware_analyis_CS658A/malware-jail",
};

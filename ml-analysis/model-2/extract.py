import os
import shutil
import pefile
import hashlib
import array
import math


def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_entropy(data):
    if len(data) == 0:
        return 0.0
    occurences = array.array('L', [0]*256)
    for x in data:
        occurences[x if isinstance(x, int) else ord(x)] += 1

    entropy = 0
    for x in occurences:
        if x:
            p_x = float(x) / len(data)
            entropy -= p_x*math.log(p_x, 2)

    return entropy


def get_resources(pe):
    """Extract resources :
    [entropy, size]"""
    resources = []
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        try:
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                data = pe.get_data(
                                    resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                size = resource_lang.data.struct.Size
                                entropy = get_entropy(data)

                                resources.append([entropy, size])
        except Exception as e:
            return resources
    return resources


def get_version_info(pe):
    """Return version infos"""
    res = {}
    for fileinfo in pe.FileInfo:
        if fileinfo.Key == 'StringFileInfo':
            for st in fileinfo.StringTable:
                for entry in st.entries.items():
                    res[entry[0]] = entry[1]
        if fileinfo.Key == 'VarFileInfo':
            for var in fileinfo.Var:
                res[var.entry.items()[0][0]] = var.entry.items()[0][1]
    if hasattr(pe, 'VS_FIXEDFILEINFO'):
        res['flags'] = pe.VS_FIXEDFILEINFO.FileFlags
        res['os'] = pe.VS_FIXEDFILEINFO.FileOS
        res['type'] = pe.VS_FIXEDFILEINFO.FileType
        res['file_version'] = pe.VS_FIXEDFILEINFO.FileVersionLS
        res['product_version'] = pe.VS_FIXEDFILEINFO.ProductVersionLS
        res['signature'] = pe.VS_FIXEDFILEINFO.Signature
        res['struct_version'] = pe.VS_FIXEDFILEINFO.StrucVersion
    return res


def extract_infos(fpath):
    res = []
    res.append(os.path.basename(fpath))
    res.append(get_md5(fpath))
    pe = pefile.PE(fpath)
    res.append(pe.FILE_HEADER.Machine)
    res.append(pe.FILE_HEADER.SizeOfOptionalHeader)
    res.append(pe.FILE_HEADER.Characteristics)
    res.append(pe.OPTIONAL_HEADER.MajorLinkerVersion)
    res.append(pe.OPTIONAL_HEADER.MinorLinkerVersion)
    res.append(pe.OPTIONAL_HEADER.SizeOfCode)
    res.append(pe.OPTIONAL_HEADER.SizeOfInitializedData)
    res.append(pe.OPTIONAL_HEADER.SizeOfUninitializedData)
    res.append(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    res.append(pe.OPTIONAL_HEADER.BaseOfCode)
    try:
        res.append(pe.OPTIONAL_HEADER.BaseOfData)
    except AttributeError:
        res.append(0)
    res.append(pe.OPTIONAL_HEADER.ImageBase)
    res.append(pe.OPTIONAL_HEADER.SectionAlignment)
    res.append(pe.OPTIONAL_HEADER.FileAlignment)
    res.append(pe.OPTIONAL_HEADER.MajorOperatingSystemVersion)
    res.append(pe.OPTIONAL_HEADER.MinorOperatingSystemVersion)
    res.append(pe.OPTIONAL_HEADER.MajorImageVersion)
    res.append(pe.OPTIONAL_HEADER.MinorImageVersion)
    res.append(pe.OPTIONAL_HEADER.MajorSubsystemVersion)
    res.append(pe.OPTIONAL_HEADER.MinorSubsystemVersion)
    res.append(pe.OPTIONAL_HEADER.SizeOfImage)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeaders)
    res.append(pe.OPTIONAL_HEADER.CheckSum)
    res.append(pe.OPTIONAL_HEADER.Subsystem)
    res.append(pe.OPTIONAL_HEADER.DllCharacteristics)
    res.append(pe.OPTIONAL_HEADER.SizeOfStackReserve)
    res.append(pe.OPTIONAL_HEADER.SizeOfStackCommit)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeapReserve)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeapCommit)
    res.append(pe.OPTIONAL_HEADER.LoaderFlags)
    res.append(pe.OPTIONAL_HEADER.NumberOfRvaAndSizes)
    res.append(len(pe.sections))
    entropy = map(lambda x: x.get_entropy(), pe.sections)
    entropyList = list(entropy)
    res.append(sum(entropyList)/float(len(entropyList)))
    res.append(min(entropyList))
    res.append(max(entropyList))
    raw_sizes = map(lambda x: x.SizeOfRawData, pe.sections)
    rawSizesList = list(raw_sizes)
    res.append(sum(rawSizesList)/float(len(rawSizesList)))
    res.append(min(rawSizesList))
    res.append(max(rawSizesList))
    virtual_sizes = map(lambda x: x.Misc_VirtualSize, pe.sections)
    virtualSizesList = list(virtual_sizes)
    res.append(sum(virtualSizesList)/float(len(virtualSizesList)))
    res.append(min(virtualSizesList))
    res.append(max(virtualSizesList))
    # Imports
    try:
        res.append(len(pe.DIRECTORY_ENTRY_IMPORT))
        imports = sum([x.imports for x in pe.DIRECTORY_ENTRY_IMPORT], [])
        res.append(len(imports))
        res.append(len(list(filter(lambda x: x.name is None, imports))))
    except AttributeError:
        res.append(0)
        res.append(0)
        res.append(0)
    # Exports
    try:
        res.append(len(pe.DIRECTORY_ENTRY_EXPORT.symbols))
    except AttributeError:
        # No export
        res.append(0)
    # Resources
    resources = get_resources(pe)
    res.append(len(resources))
    if len(resources) > 0:
        entropy = map(lambda x: x[0], resources)
        entropyList = list(entropy)
        res.append(sum(entropyList)/float(len(entropyList)))
        res.append(min(entropyList))
        res.append(max(entropyList))
        sizes = map(lambda x: x[1], resources)
        sizesList = list(sizes)
        res.append(sum(sizesList)/float(len(sizesList)))
        res.append(min(sizesList))
        res.append(max(sizesList))
    else:
        res.append(0)
        res.append(0)
        res.append(0)
        res.append(0)
        res.append(0)
        res.append(0)

    # Load configuration size
    try:
        res.append(pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size)
    except AttributeError:
        res.append(0)

    # Version configuration size
    try:
        version_infos = get_version_info(pe)
        res.append(len(version_infos.keys()))
    except AttributeError:
        res.append(0)
    return res


if __name__ == '__main__':
    output = "data_demo.csv"
    csv_delimiter = "|"
    columns = [
        "Name",
        "md5",
        "Machine",
        "SizeOfOptionalHeader",
        "Characteristics",
        "MajorLinkerVersion",
        "MinorLinkerVersion",
        "SizeOfCode",
        "SizeOfInitializedData",
        "SizeOfUninitializedData",
        "AddressOfEntryPoint",
        "BaseOfCode",
        "BaseOfData",
        "ImageBase",
        "SectionAlignment",
        "FileAlignment",
        "MajorOperatingSystemVersion",
        "MinorOperatingSystemVersion",
        "MajorImageVersion",
        "MinorImageVersion",
        "MajorSubsystemVersion",
        "MinorSubsystemVersion",
        "SizeOfImage",
        "SizeOfHeaders",
        "CheckSum",
        "Subsystem",
        "DllCharacteristics",
        "SizeOfStackReserve",
        "SizeOfStackCommit",
        "SizeOfHeapReserve",
        "SizeOfHeapCommit",
        "LoaderFlags",
        "NumberOfRvaAndSizes",
        "SectionsNb",
        "SectionsMeanEntropy",
        "SectionsMinEntropy",
        "SectionsMaxEntropy",
        "SectionsMeanRawsize",
        "SectionsMinRawsize",
        "SectionMaxRawsize",
        "SectionsMeanVirtualsize",
        "SectionsMinVirtualsize",
        "SectionMaxVirtualsize",
        "ImportsNbDLL",
        "ImportsNb",
        "ImportsNbOrdinal",
        "ExportNb",
        "ResourcesNb",
        "ResourcesMeanEntropy",
        "ResourcesMinEntropy",
        "ResourcesMaxEntropy",
        "ResourcesMeanSize",
        "ResourcesMinSize",
        "ResourcesMaxSize",
        "LoadConfigurationSize",
        "VersionInformationSize",
        "legitimate"
    ]

    ff = open(output, "w")
    ff.write(csv_delimiter.join(columns) + "\n")

    for ffile in os.listdir('DemoExamples/WinBenignExecutables'):
        print(ffile)
        try:
            res = extract_infos(os.path.join('DemoExamples/WinBenignExecutables', ffile))
            res.append(1)
            ff.write(csv_delimiter.join(map(lambda x: str(x), res)) + "\n")
        except pefile.PEFormatError:
            print('\t -> Bad PE format in benign folder')

    for ffile in os.listdir('DemoExamples/WinMaliciousExecutables'):
        print(ffile)
        try:
            res = extract_infos(os.path.join('DemoExamples/WinMaliciousExecutables', ffile))
            res.append(0)

            ff.write(csv_delimiter.join(map(lambda x: str(x), res)) + "\n")
            shutil.copy("DemoExamples/WinMaliciousExecutables/"+ffile, "DemoExamples/2/")
        except pefile.PEFormatError:
            print('\t -> Bad PE format in malicious folder')
        except:
            print('\t -> Weird error in malicious folder')
    ff.close()

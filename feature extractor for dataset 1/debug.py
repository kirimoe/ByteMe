import pefile

pe = pefile.PE('./calc.exe')

extracted_features = {}

def extract_other_features(features, header):

    if hasattr(pe, header):
        #get header
        if header == 'FILE_HEADER':
            _header = pe.FILE_HEADER
        elif header == 'OPTIONAL_HEADER':
            _header = pe.OPTIONAL_HEADER
        elif header == 'DOS_HEADER':
            _header = pe.DOS_HEADER
        
        for feature in features:
            try:
                value = getattr(_header, feature)
            except AttributeError:
                value = None
            extracted_features[feature] = value
    else:
        for feature in features:
            extracted_features[feature] = None

    #print(extracted_features)


def extract_section_features():
    features = ['PointerToLinenumbers', 'NumberOfLinenumbers', 'Characteristics', 'PointerToRawData', 'SizeOfRawData', 'VirtualAddress', 'Misc_VirtualSize', 'NumberOfRelocations', 'PointerToRelocations']

    sections = ['text', 'data', 'pdata', 'idata', 'rdata', 'rsrc', 'reloc', 'edata', 'tls', 'bss']

    for i, section_name in enumerate(sections):
        if i < len(pe.sections):
            section = pe.sections[i]
            for feature in features:
                try:
                    value = getattr(section, feature)
                except AttributeError:
                    value = None
                extracted_features[f"{section_name}_{feature}"] = value
        else:
            for feature in features:
                extracted_features[f"{section_name}_{feature}"] = None

    #print(extracted_features)



def our_PEFeatureExtractor():

    # extract other features
    optional_header_features = ['NumberOfRvaAndSizes', 'DllCharacteristics', 'MajorOperatingSystemVersion', 'AddressOfEntryPoint', 'MinorSubsystemVersion', 'CheckSum', 'Subsystem', 'MajorImageVersion', 'SizeOfInitializedData', 'BaseOfCode', 'MajorLinkerVersion', 'SizeOfUninitializedData', 'SizeOfImage', 'SizeOfHeapCommit', 'SizeOfStackReserve', 'MajorSubsystemVersion', 'SectionAlignment', 'FileAlignment', 'MinorLinkerVersion', 'SizeOfCode', 'LoaderFlags', 'MinorImageVersion', 'SizeOfHeapReserve', 'SizeOfHeaders', 'MinorOperatingSystemVersion', 'ImageBase']
    file_header_features = ['NumberOfSections', 'PointerToSymbolTable', 'SizeOfOptionalHeader', 'Machine', 'Type', 'NumberOfSymbols', 'Reserved1', 'Characteristics', 'TimeDateStamp']
    dos_header_features = ['Magic', 'e_sp', 'e_oeminfo', 'e_lfanew', 'e_ip', 'e_magic', 'e_cs', 'e_oemid', 'e_cblp', 'e_maxalloc', 'e_crlc', 'e_minalloc', 'e_csum', 'e_ovno', 'e_cp', 'e_ss', 'e_lfarlc', 'e_cparhdr']

    headers = {'OPTIONAL_HEADER': optional_header_features, 'FILE_HEADER': file_header_features, 'DOS_HEADER': dos_header_features}

    for header, features in headers.items(): 
        extract_other_features(features, header)


    #extract section features
    extract_section_features()

    #return all features
    return extracted_features


if __name__ == '__main__':
    features = our_PEFeatureExtractor()

    #print features
    for key, values in features.items():
        print(key, values)
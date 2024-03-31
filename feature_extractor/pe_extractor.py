import lief
import re
import math
import json
import pandas as pd

class PEAttributeExtractor:
    libraries = ""
    functions = ""
    exports = ""

    def __init__(self, bytez):
        self.bytez = bytez
        self.lief_binary = lief.PE.parse(list(bytez))
        self.attributes = {}

    def extract_string_metadata(self):
        paths = re.compile(b'c:\\\\', re.IGNORECASE)
        urls = re.compile(b'https?://', re.IGNORECASE)
        registry = re.compile(b'HKEY_')
        mz = re.compile(b'MZ')
        return {
            'string_paths': len(paths.findall(self.bytez)),
            'string_urls': len(urls.findall(self.bytez)),
            'string_registry': len(registry.findall(self.bytez)),
            'string_MZ': len(mz.findall(self.bytez))
        }

    def extract_entropy(self):
        if not self.bytez:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(self.bytez.count(bytes(x))) / len(self.bytez)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def extract(self):
        try:
            has_signature = int(self.lief_binary.has_signature)
        except:
            has_signature = 0

        self.attributes.update({
            "virtual_size": self.lief_binary.virtual_size,
            "has_debug": int(self.lief_binary.has_debug),
            "imports": len(self.lief_binary.imports),
            "exports": len(self.lief_binary.exported_functions),
            "has_relocations": int(self.lief_binary.has_relocations),
            "has_resources": int(self.lief_binary.has_resources),
            "has_signature": has_signature,
            "has_tls": int(self.lief_binary.has_tls),
            "symbols": len(self.lief_binary.symbols),
        })

        self.attributes.update({
            "timestamp": self.lief_binary.header.time_date_stamps,
            "machine": str(self.lief_binary.header.machine),
            "numberof_sections": self.lief_binary.header.numberof_sections,
            "characteristics_list": " ".join([str(c).replace("HEADER_CHARACTERISTICS.", "") for c in self.lief_binary.header.characteristics_list])
        })

        try:
            baseof_data = self.lief_binary.optional_header.baseof_data
        except:
            baseof_data = 0

        self.attributes.update({
            "dll_characteristics_list": " ".join([str(d).replace("DLL_CHARACTERISTICS.", "") for d in self.lief_binary.optional_header.dll_characteristics_lists]),
            "magic": str(self.lief_binary.optional_header.magic).replace("PE_TYPE.", ""),
            "major_image_version": self.lief_binary.optional_header.major_image_version,
            "minor_image_version": self.lief_binary.optional_header.minor_image_version,
            "major_linker_version": self.lief_binary.optional_header.major_linker_version,
            "minor_linker_version": self.lief_binary.optional_header.minor_linker_version,
            "major_operating_system_version": self.lief_binary.optional_header.major_operating_system_version,
            "minor_operating_system_version": self.lief_binary.optional_header.minor_operating_system_version,
            "major_subsystem_version": self.lief_binary.optional_header.major_subsystem_version,
            "minor_subsystem_version": self.lief_binary.optional_header.minor_subsystem_version,
            "sizeof_code": self.lief_binary.optional_header.sizeof_code,
            "sizeof_headers": self.lief_binary.optional_header.sizeof_headers,
        })

        self.attributes.update({
            "entropy": self.extract_entropy()
        })

        self.attributes.update(self.extract_string_metadata())

        if self.lief_binary.has_imports:
            self.libraries = " ".join([l for l in self.lief_binary.libraries])
            self.functions = " ".join([f.name for f in self.lief_binary.imported_functions])
        self.attributes.update({"functions": self.functions, "libraries": self.libraries})

        if self.lief_binary.has_exports:
            self.exports = " ".join([f.name for f in self.lief_binary.exported_functions])
        self.attributes.update({"exports_list": self.exports})

        return self.attributes

# Example usage
if __name__ == "__main__":
    # Read PE file
    with open("CFFLAT.exe", "rb") as f:
        bytez = f.read()

    # Create PEAttributeExtractor instance and extract features
    pe_att_ext = PEAttributeExtractor(bytez)
    extracted_features = pe_att_ext.extract()

    # Print extracted features
    print('Normal Features:\n\n')
    for key, value in extracted_features.items():
        print(f"{key}: {value}")

    print('\n\nJSON:\n\n')
    json_attributes = json.dumps(extracted_features)
    print(json_attributes)

    print('\n\nPandas Dataframe:\n\n')
    pd.set_option('display.max_columns', None)
    atts = pd.DataFrame([extracted_features])
    print(atts)
import yara
import sys

# Define the path to rules folder
RULES_PATH = './packer_cryptor_detect/rules/'

# List of packers/cryptors to detect
PACKERS = [
    'AHTeam', 'Armadillo', 'Stelth', 'yodas', 'ASProtect', 'ACProtect', 'PEnguinCrypt',
    'UPX', 'Safeguard', 'VMProtect', 'Vprotect', 'WinLicense', 'Themida', 'WinZip', 'WWPACK',
    'Y0da', 'Pepack', 'Upack', 'TSULoader', 'SVKP', 'Simple', 'StarForce', 'SeauSFX', 'RPCrypt',
    'Ramnit', 'RLPack', 'ProCrypt', 'Petite', 'PEShield', 'Perplex', 'PELock', 'PECompact',
    'PEBundle', 'RLPack', 'NsPack', 'Neolite', 'Mpress', 'MEW', 'MaskPE', 'ImpRec', 'kkrunchy',
    'Gentee', 'FSG', 'Epack', 'DAStub', 'Crunch', 'CCG', 'Boomerang', 'ASPAck', 'Obsidium',
    'Ciphator', 'Phoenix', 'Thoreador', 'QinYingShieldLicense', 'Stones', 'CrypKey', 'VPacker',
    'Turbo', 'codeCrypter', 'Trap', 'beria', 'YZPack', 'crypt', 'crypt', 'pack', 'protect', 'tect', 'Alienyze'
]

def setup_rules():
    #"""Compile YARA rules."""
    try:
        peid_rules = yara.compile(RULES_PATH + 'peid.yar')
        packer_rules = yara.compile(RULES_PATH + 'packer.yar')
        crypto_rules = yara.compile(RULES_PATH + 'crypto_signatures.yar')
        return peid_rules, packer_rules, crypto_rules
    except yara.Error as e:
        print(f"Error while compiling YARA rules: {e}")
        return None, None, None

def detect_cryptors(exe_file_path, crypto_rules):
    #"""Detect cryptors using YARA rules."""
    cryptor_names = []
    try:
        matches = crypto_rules.match(exe_file_path)
        if matches:
            for match in matches:
                cryptor_names.append(match.rule)
    except yara.Error as e:
        print(f"Error while detecting cryptors: {e}")
    return cryptor_names

def detect_packers(exe_file_path, packer_rules):
    #"""Detect packers using YARA rules."""
    packer_names = []
    try:
        matches = packer_rules.match(exe_file_path)
        if matches:
            for match in matches:
                packer_names.append(match.rule)
    except yara.Error as e:
        print(f"Error while detecting packers: {e}")
    return packer_names


### Removing pied as of now

# def detect_peid_packers(exe_file_path, peid_rules):
#     """Detect packers using PEiD YARA rules."""
#     packer_names = []
#     try:
#         matches = peid_rules.match(exe_file_path)
#         if matches:
#             for match in matches:
#                 for packer in PACKERS:
#                     if packer.lower() in match.rule.lower():
#                         packer_names.append(packer)
#     except yara.Error as e:
#         print(f'Error: {e}')
#     return packer_names

def analyze_file(exe_file_path):
    #"""Analyze an executable file."""
    peid_rules, packer_rules, crypto_rules = setup_rules()
    #if not all((peid_rules, packer_rules, crypto_rules)):
    #    return

    packer_names = detect_packers(exe_file_path, packer_rules)
    cryptor_names = detect_cryptors(exe_file_path, crypto_rules)

    #print(type(packer_names), type(cryptor_names))
    
    #peid_packer_names = detect_peid_packers(exe_file_path, peid_rules)

    #print("Packers detected:", packer_names if packer_names else "None")
    #print("Cryptors detected:", cryptor_names if cryptor_names else "None")
    #print("PEiD Packers detected:", peid_packer_names if peid_packer_names else "None")

    if len(packer_names) > 0 or len(cryptor_names) > 0:
        return 1
    elif len(packer_names) > 0 and len(cryptor_names) > 0:
        return 2
    else:
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <exe_file_path>")
        sys.exit(1)
    analyze_file(sys.argv[1])
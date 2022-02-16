from pathlib import Path

thisDir = Path(__file__).parent


def tryIntoNum(v: str):
	try:
		return int(v)
	except ValueError:
		try:
			return float(v)
		except ValueError:
			return v


def numericDict(d):
	return {k: tryIntoNum(v) for k, v in d.items()}


def loadTSV(p: Path):
	return [numericDict(el) for el in csv.DictReader(p.read_text().splitlines(), dialect=csv.excel_tab)]


def loadProprietaryNames():
	proprietary_names = loadTSV(thisDir / "proprietary_names.tsv")

	idx = {}
	revIdx = {}

	for el in proprietary_names:
		print(el)
		idx[el["name_smsd"]] = el["name"]
		revIdx[el["name"]] = el["name_smsd"]

	return idx, revIdx


proprietaryNameToName, nameToProprietaryName = loadProprietaryNames()


def loadUnknownMotorsSpecs():
	unknown_motors = loadTSV(thisDir / "unknown_motors.tsv")

	res = {}
	for el in unknown_motors:
		iD = el["SMSD-8.0LAN"] - 1
		del el["SMSD-8.0LAN"]
		res[iD] = el
	return res


unknown_motors = loadUnknownMotorsSpecs()


def loadMotorNames():
	motorNames = loadTSV(thisDir / "motors_names.tsv")
	nameToEight = {}
	eightToName = [None] * len(motorNames)

	fourToEight = [None] * len(motorNames)
	eightToFour = [None] * len(motorNames)

	for el in motorNames:
		eightNo = el["SMSD-8.0LAN"] - 1
		connT = el["connection_type"] == "p"
		if el["name"]:
			nameToEight[(el["name"], connT)] = eightNo
			eightToName[eightNo] = (el["name"], connT)

		if el["SMSD-4.2LAN"]:
			fourNo = el["SMSD-4.2LAN"] - 1
			fourToEight[fourNo] = eightNo
			eightToFour[eightNo] = fourNo

	return nameToEight, eightToName, fourToEight, eightToFour


nameToEight, eightToName, fourToEight, eightToFour = loadMotorNames()


def getMotorIdByNameAndType(name: str, isParallel: bool = False, version: int = 8):
	eightNum = nameToEight[name, isParallel] + 1
	if version == 4:
		return eightToFour[eightNum]
	return eightNum


def motorIdIntoNameAndConnectionType(motorId: int, version: int = 8):
	motorId -= 1

	if version == 4:
		motorId = fourToEight[motorId]

	return eightToName[motorId]

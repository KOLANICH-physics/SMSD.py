#!/usr/bin/env python3

import ast

from pathlib import Path

from SMSD.formats import rawHashTable
from PerfectPrecomputedHashtable import POWConfig, genPerfectHashtable
from PerfectPrecomputedHashtable.codegen import genCode, GenCfg, takeFromFile

def o2b(s: str) -> bytes:
	if not isinstance(s, bytes):
		s = s.encode("cp1251")
	return s

def valueASTGen(cmd):
	enumName = cmd.__class__.__name__
	valueName = cmd.name
	return ast.Attribute(
		value=ast.Name(id=enumName, ctx=ast.Load()),
		attr=valueName, ctx=ast.Load()
	)

fromThisFile = takeFromFile(Path(__file__), {o2b.__name__})

powCfg = POWConfig.fromDict({"nonce": 0x754d60b8, "span": 0xf1222157, "reducer": 8, "reduced_span": 168})

"""
Checked all the nonces up to 0x90000000. The most remarkable results are:
{"nonce": 0x259eebf1, "span": 0xfbe6997f, "reducer": 13, "reduced_span": 171} utf-8
{"nonce": 0x2eebe99e, "span": 0xf9a8a317, "reducer": 0, "reduced_span": 174} cp1251
{"nonce": 0x431dfcac, "span": 0xecab1070, "reducer": 15, "reduced_span": 174} cp1251
{"nonce": 0x52fafdf9, "span": 0xf946c235, "reducer": 16, "reduced_span": 169} cp1251
{"nonce": 0x754d60b8, "span": 0xf1222157, "reducer": 8, "reduced_span": 168} cp1251

"""

if __name__ == "__main__":
	g = genPerfectHashtable(powCfg, rawHashTable, o2b)

	print(genCode(g, GenCfg(
		valueASTGen=valueASTGen,
		preamble = [
			ast.ImportFrom(module='commands', names=[ast.alias(name='*')], level=1),
			ast.ImportFrom(module='enum', names=[ast.alias(name='Enum')], level=0),
		],
		o2b = fromThisFile["o2b"]
	)))

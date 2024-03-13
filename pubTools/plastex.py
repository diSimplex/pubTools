
import os
import sys
import yaml

import plasTeX.client

def getMagicComments(texFilePath) :
  # read the beginning of the file looking for TeX-Magic comments
  with open(texFilePath) as tf :
    while True :
      aLine = tf.readline()
      if not aLine : break
      aLine = aLine.strip()
      if not aLine.startswith('%') :
        if len(aLine) : break
        else : continue
      if not aLine.find('=') : continue
      lineFields = aLine.split('=')
      aKey = lineFields[0].lower()
      if len(lineFields) < 2 : continue
      aValue = lineFields[1].strip()
      if -1 < aKey.find('!lpil') :
        if -1 < aKey.find('preamble') :
          config['preamble'] = aValue
        if -1 < aKey.find('postamble') :
          config['postamble'] = aValue
      if -1 < aKey.find('!tex') and -1 < aKey.find('program') :
        config['program'] = aValue

def cli() :

  buildDir = os.path.join('build', 'web')
  os.makedirs(buildDir, exist_ok=True)

  pArgv = []
  lArgv =  [ f"--dir={buildDir}", "--plugins", "lpilPlasTeX", "--" ]
  #lArgv =  []
  fArgv = []
  filePath = sys.argv[len(sys.argv)-1]
  if filePath == '--help' or filePath == '-h' :
    pArgv.append(filePath)
    filePath = None
  nextIsConfig = False
  verbose = False
  for anArg in sys.argv[1:len(sys.argv)-1] :
    if anArg == '--verbose' or anArg == '-v' :
      verbose = True
      continue
    if anArg == '--config' or anArg == '-c' :
      nextIsConfig = True
      continue
    if nextIsConfig :
      nextIsConfig = False
      pArgv.extend(['--config', anArg])
      continue
    if anArg == '--help' or anArg == '-h' :
      pArgv.append(anArg)
      continue
    pArgv.append(anArg)
  theArgs = pArgv + lArgv + fArgv
  theArgs.append(filePath)
  if verbose :
    print("-------------------")
    print(yaml.dump(theArgs))
    print("-------------------")
  try :
    plasTeX.client.main(theArgs)
  except KeyboardInterrupt :
    pass

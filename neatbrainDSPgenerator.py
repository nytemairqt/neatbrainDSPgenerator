#networkbuilder

string = '<?xml version="1.0" encoding="UTF-8"?>'
PATH = 'D:/Documents/HISE/neatbraintestingSCRIPTNODE/DspNetworks/Networks'

import modules
from hyperparameters import *

file = open(f'{PATH}/NEATBrain_Achromic.xml', 'w')

# TO DO

# Scale ratios to be between 0 & 1 (divide by 100)
# Then scale output of sliderpack back to the raw ratio value
# take Value of Sliderpack and make it 100

# stuff gets normalized when you connect it to a cable :))))))

# should random pitch go flat? as in below value 0?

# random global
	# note on functionality, set fixed cable value to random value between 0 & 1 
	# plug cable into PMA add and make sure it scales properly

# IMPORTANT: uncomment out filters, tanh etc etc

# by exposing the sliderpacks to the end user, we could create presets that sound like different instruments...
# just save the ratios as a json object or array 
# velocity PITCH
# velocity FILTER
# velocity AMPLITUDE (maybe)
# pitch bend (global pitch mod i think)
# get pitch mod working, something to do with no_midi maybe idk

# Instantiate XML Doc

NETWORK_START = []
NETWORK_PARAMS = []
NETWORK_END = []

NETWORK_START.append('<?xml version="1.0" encoding="UTF-8"?>')
NETWORK_START.append(f'<Network ID="{INSTRUMENT_NAME}" AllowPolyphonic="1" Version="0.0.0">')
NETWORK_START.append(f'<Node FactoryPath="container.chain" ID="{INSTRUMENT_NAME}" Bypassed="0" ShowParameters="1">')
NETWORK_START.append('<Nodes>')
NETWORK_START.append('<!-- Begin Node Tree -->')

NETWORK_PARAMS.append('</Nodes> <!--End Master Nodes -->')
NETWORK_PARAMS.append('<!-- Master Params go Here -->')
NETWORK_PARAMS.append('<Parameters>')
NETWORK_PARAMS.append('</Parameters>')

NETWORK_END.append('<!-- End Node Tree & Close Network-->')
NETWORK_END.append('</Node>')
NETWORK_END.append('</Network>')

# Parameters

# Min/Max Values for Normalizing

denorm_ratios = {
	'min_ratio_L' : min(RATIOS_L),
	'max_ratio_L' : max(RATIOS_L),
	'min_ratio_R' : min(RATIOS_R),
	'max_ratio_R' : max(RATIOS_R),
}

for ratio in denorm_ratios:
	modules.create_parameter(NETWORK_PARAMS, ratio, denorm_ratios[ratio], denorm_ratios[ratio], 0.01, denorm_ratios[ratio])


parameters = {	
	'stiffness' : [0.0, 1.0, 0.01, 0.0],
	'stiffnessType' : [0.0, 1.0, 1.0, 0.0],
	'pitchVelocity' : [0.0, 1.0, 0.01, 0.0],
	'pitchFalloffIntensity' : [0.0, 1.0, 0.01, PITCH_FALLOFF_INTENSITY],
	'pitchFalloffDecay' : [0, 40000, 1, PITCH_FALLOFF_DECAY],
	'pitchRandomIntensity' : [0.0, 1.0, 0.01, 0.1],
	'pitchRandomGlobalBang' : [0.0, 1.0, 0.01, 0.1],
	'pitchRandomGlobalIntensity' : [0.0, 1.0, 0.01, 0.1],
	'filterFalloffDecay' : [0, 40000, 1, FILTER_FALLOFF_DECAY],
	'filterStaticFrequency' : [500, 5000, 1, FILTER_STATIC_FREQUENCY]
}

for param in parameters:
	modules.create_parameter(NETWORK_PARAMS, param, parameters[param][0], parameters[param][1], parameters[param][2], parameters[param][3])
	
# Connections

if __name__=="__main__":
	# be careful using restoreState() on the scriptnode synth

	# Instantiate Nodes

	nodes = []
	
	ahdsr_filter = modules.add_AHDSR("ahdsrFilter", 5.0, 1.0, FILTER_FALLOFF_DECAY, 0.0, 50) # A AL D S R 
	sliderpack_ratiosL = modules.add_clone_sliderpack("ratiosL", NUM_MODES)
	sliderpack_ratiosR = modules.add_clone_sliderpack("ratiosR", NUM_MODES)

	nodes.append(modules.open_chain('ahdsrs', 'container.split', folded=1))
	nodes.append(ahdsr_filter)
	nodes.append(modules.close_chain('ahdsrs'))
	nodes.append(modules.open_chain('ratioChains', 'container.split'))
	nodes.append(sliderpack_ratiosL)
	nodes.append(sliderpack_ratiosR)
	nodes.append(modules.close_chain('ratioChains'))

	# Parameter Nodes for Clones

	nodes.append(modules.open_chain('global_params', 'container.split', folded=0))

	cable_pitchFalloffIntensity = modules.add_clone_cable(f'pitchFalloffIntensity', NUM_MODES, mode="Fixed", use_container=True)		
	cable_pitchFalloffDecay = modules.add_clone_cable(f'pitchFalloffDecay', NUM_MODES, mode="Fixed", use_container=True)	
	cable_pitchRandomIntensity = modules.add_clone_cable(f'pitchRandomIntensity', NUM_MODES, mode="Fixed", use_container=True)	
	nodes.append(cable_pitchFalloffIntensity)
	nodes.append(cable_pitchFalloffDecay)
	nodes.append(cable_pitchRandomIntensity)

	# Random Global
	cable_randomGlobal = modules.add_clone_cable(f'randomGlobal', NUM_MODES, value=1.0, mode="Fixed", use_container=True)
	nodes.append(cable_randomGlobal)


	# Random Single
	cable_randomSingle = modules.add_clone_cable(f'randomSingle', NUM_MODES, value=1.0, mode="Random", use_container=False)
	nodes.append(cable_randomSingle)	

	# End Params
	nodes.append(modules.close_chain('global_params'))

	# Begin Oscillators
	if STEREO_INSTRUMENT:
		nodes.append(modules.open_chain("multiChannel", "container.multi", folded=1))

	# Left Channel
	nodes.append(modules.open_chain("chainL", "container.chain"))

	# Cloner Object
	nodes.append(modules.open_cloner('clonerL'))

	# Left Channel (Or Center if !Stereo)
	for i in range(NUM_MODES):
		nodes.append([f'<!-- Begin Clone Child -->'])
		nodes.append([f'<Node ID="sineL_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
		nodes.append([f'<Nodes>'])

		# Need these declared...
		ahdsr_pitch = modules.add_AHDSR(f"sineL_{i}_ahdsrPitch", 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 

		pma_random = modules.add_pma(f'sineL_{i}_pma_random', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, multiply_max=1.0, add_max=1.0)
		pma_randomGlobal = modules.add_pma(f'sineL_{i}_pma_randomGlobal', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, multiply_max=1.0, add_max=1.0)

		# Base Ratio Sliderpacks plug into this:
		denormalizer = modules.add_minmax(f'sineL_{i}_denormalizer', denorm_ratios["min_ratio_L"], denorm_ratios["max_ratio_L"])

		pma_output = modules.add_pma(f'sineL_{i}_pma_output', 1.0, 1.0, 0.0, scaled=False, value_max=100.0)
		sine = modules.add_sine(f'sineL_{i}', 1.0)

		nodes.append(ahdsr_pitch)		
		nodes.append(pma_random)
		nodes.append(pma_randomGlobal)
		nodes.append(denormalizer)
		nodes.append(pma_output)
		nodes.append(sine)

		nodes.append([f'</Nodes>'])
		nodes.append([f'<Parameters/>'])
		nodes.append([f'</Node>']) # Manually Close
		nodes.append([f'<!-- End Clone Child -->'])

		# ============================
		# ONLY CONNECT THE FIRST CLONE
		# ============================
		if i == 0:
			modules.connect_module(cable_pitchFalloffIntensity, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'AttackLevel')	
			modules.connect_module(cable_pitchFalloffDecay, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'Decay')
			modules.connect_module(cable_pitchRandomIntensity, '<ModulationTargets>', f'sineL_{i}_bangInput', 'Value')
			modules.connect_module(cable_randomSingle, '<ModulationTargets>', f'sineL_{i}_pma_random', 'Add')	
			modules.connect_module(cable_randomGlobal, '<ModulationTargets>', f'sineL_{i}_pma_randomGlobal', 'Add')								

		modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineL_{i}_pma_random', 'Value')		
		modules.connect_module(denormalizer, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Value')
		modules.connect_module(pma_random, '<ModulationTargets>', f'sineL_{i}_pma_randomGlobal', 'Value')		
		modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Add')
		modules.connect_module(pma_output, '<ModulationTargets>', f'sineL_{i}', 'Freq Ratio')

	nodes.append(modules.close_cloner("clonerL", NUM_MODES))
	
	if STEREO_INSTRUMENT:
		nodes.append(modules.add_jpanner("jpanLeft", -1.0))

	nodes.append(modules.close_chain("chainL"))

	if STEREO_INSTRUMENT:
		# Right Channel
		nodes.append(modules.open_chain("chainR", "container.chain"))

		# Cloner Object

		nodes.append(modules.open_cloner('clonerR'))

		# Clone Chain 

		
		for i in range(NUM_MODES):
			nodes.append([f'<!-- Begin Clone Child -->'])
			#nodes.append([f'<Node ID="clone_child" FactoryPath="container.chain" Bypassed="0">'])
			nodes.append([f'<Node ID="sineR_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
			nodes.append([f'<Nodes>'])

			#nodes.append(modules.open_chain(f'sineR_chain', 'container.chain', folded=1))
			#nodes.append(modules.add_bang(f'sineR_{i}_bangInput', 0.1)) # connect to parameter "Random Strength"
			#nodes.append(modules.add_cable_expr(f'sineR_{i}_cable', 'Math.random() * input'))
			#nodes.append(modules.add_bang(f'sineR_{i}_bangOutput', 1.0))
			nodes.append(modules.add_pma(f'sineR_{i}_pma_ahdsrStrength', 1.0, PITCH_FALLOFF_INTENSITY, 1.0)) # Connect Multiply to "Strength" Param, connect Value to AHDSR_Pitch
			nodes.append(modules.add_pma(f'sineR_{i}_pma_ahdsr', 1.0, 1.0, 1.0)) # Connect Value to "Modes{i}", connect Add to previous PMA
			nodes.append(modules.add_pma(f'sineR_{i}_pma_random', 1.0, 1.0, 0.0))
			nodes.append(modules.add_pma(f'sineR_{i}_pma_randomGlobal', 1.0, 1.0, 0.0))
			nodes.append(modules.add_pma(f'sineR_{i}_pma_output', 1.0, 1.0, 0.0))
			nodes.append(modules.add_sine(f'sineR_{i}', 1.0))
			#nodes.append(modules.close_chain(f'sineR_chain_{i}'))

			nodes.append([f'</Nodes>'])
			nodes.append([f'<Parameters/>'])
			nodes.append([f'</Node>']) # Manually Close
			nodes.append([f'<!-- End Clone Child -->'])

			# Connect Sliderpacks
			#modules.connect_parameter(nodes, 'sliderpack_pitchRandomIntensity', f'sineR_{i}_bangInput', 'Value')

		nodes.append(modules.close_cloner("clonerR", NUM_MODES))


		nodes.append(modules.add_jpanner("jpanRight", 1.0))
		nodes.append(modules.close_chain("chainR"))
		nodes.append(modules.close_chain("multiChannel"))

	# Stiffness

	'''
	nodes.append(modules.open_chain("tanhSplit", "container.split"))
	nodes.append(modules.open_chain("tanhOff", "container.chain"))
	nodes.append(modules.add_gain("tanhDry", invert=True))
	nodes.append(modules.close_chain("tanhOff"))
	nodes.append(modules.open_chain("tanhOn", "container.chain"))
	nodes.append(modules.add_switcher("stiffnessSwitch"))
	nodes.append(modules.add_gain("tanhWet", invert=False))
	nodes.append(modules.close_chain("tanhOn"))
	nodes.append(modules.close_chain("tanhSplit"))

	# Filters
	nodes.append(modules.add_filter('lowPass', 2000))
	nodes.append(modules.add_filter('ahdsrFilter', 4000))
	modules.connect_module(ahdsr_filter, '<!-- CV -->', 'ahdsrFilter', 'Frequency')	
	'''

	# Connect Sine Waves

	modules.connect_module(sliderpack_ratiosL, '<ModulationTargets>', 'sineL_pma_output', 'Value')
	#modules.connect_module(sliderpack_ratiosR, '<ModulationTargets>', 'sineR_pma_output', 'Value')

	# Connect Global Parameters		
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'cable_pitchFalloffIntensity', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'cable_pitchFalloffDecay', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomIntensity', 'cable_randomSingle', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalBang', 'cable_randomGlobal', 'Value')
	#modules.connect_parameter(NETWORK_PARAMS, 'pitchMod_randomGlobal', 'cable_randomGlobal', 'Value')

	#modules.connect_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 'ahdsrFilter', 'Decay')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhDry', 'Gain')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhWet', 'Gain')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffnessType', 'stiffnessSwitch', 'Type')
	#modules.connect_parameter(NETWORK_PARAMS, 'filterStaticFrequency', 'lowPass', 'Frequency')

	# Start Writers

	for text in NETWORK_START:
		file.write(f'{text}\n')

	for node in nodes:
		for text in node:
			file.write(f'{text}\n')

	for text in NETWORK_PARAMS:
		file.write(f'{text}\n')
	for text in NETWORK_END:
		file.write(f'{text}\n')

	file.close()

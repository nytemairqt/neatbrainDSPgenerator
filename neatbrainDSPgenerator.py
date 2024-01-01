#networkbuilder

string = '<?xml version="1.0" encoding="UTF-8"?>'
#PATH = 'D:/Documents/HISE/neatbraintestingSCRIPTNODE/DspNetworks/Networks'
PATH = 'D:/Documents/HISE/neatbraininstrument/DspNetworks/Networks'

import modules
from hyperparameters import *

file = open(f'{PATH}/NEATBrain_Achromic.xml', 'w')

# TO DO

# Connect ratios to front-end
# Scale ratios to be between 0 & 1
# Z = (X - min(x)) / (max(x) - min(x))
# denormalize with fancy node

# Pitch Bend
# Pitch Velocity
# Filter Velocity
# Amplitude Velocity

# IMPORTANT: uncomment out filters, tanh etc etc

# by exposing the sliderpacks to the end user, we could create presets that sound like different instruments...
# just save the ratios as a json object or array 

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
	'pitchRandomGlobalBang' : [-1.0, 1.0, 0.01, 0.1],
	'pitchRandomGlobalIntensity' : [0.0, 1.0, 0.01, 0.1],
	'pitchRandomSingleIntensity' : [0.0, 1.0, 0.01, 0.1],
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

	nodes.append(modules.open_chain('global_params', 'container.split', folded=1))

	cable_pitchFalloffIntensityL = modules.add_clone_cable(f'pitchFalloffIntensityL', NUM_MODES, mode="Fixed", use_container=True)		
	cable_pitchFalloffIntensityR = modules.add_clone_cable(f'pitchFalloffIntensityR', NUM_MODES, mode="Fixed", use_container=True)		
	cable_pitchFalloffDecayL = modules.add_clone_cable(f'pitchFalloffDecayL', NUM_MODES, mode="Fixed", use_container=True)	
	cable_pitchFalloffDecayR = modules.add_clone_cable(f'pitchFalloffDecayR', NUM_MODES, mode="Fixed", use_container=True)	
	nodes.append(cable_pitchFalloffIntensityL)
	nodes.append(cable_pitchFalloffIntensityR)
	nodes.append(cable_pitchFalloffDecayL)
	nodes.append(cable_pitchFalloffDecayR)

	# Random Global
	nodes.append(modules.open_chain('cable_randomGlobalContainer', 'container.chain', folded=0))
	cable_randomGlobalL = modules.add_clone_cable(f'randomGlobalL', NUM_MODES, value=1.0, min_value=-1.0, max_value=1.0, mode="Fixed", use_container=True)
	cable_randomGlobalR = modules.add_clone_cable(f'randomGlobalR', NUM_MODES, value=1.0, min_value=-1.0, max_value=1.0, mode="Fixed", use_container=True)
	cable_randomGlobalIntensityL = modules.add_clone_cable(f'randomGlobalIntensityL', NUM_MODES, value=1.0, min_value=0.0, max_value=1.0, mode="Fixed", use_container=True)
	cable_randomGlobalIntensityR = modules.add_clone_cable(f'randomGlobalIntensityR', NUM_MODES, value=1.0, min_value=0.0, max_value=1.0, mode="Fixed", use_container=True)
	nodes.append(cable_randomGlobalL)
	nodes.append(cable_randomGlobalR)
	nodes.append(cable_randomGlobalIntensityL)
	nodes.append(cable_randomGlobalIntensityR)
	nodes.append(modules.close_chain('cable_randomGlobalContainer'))


	# Random Single
	nodes.append(modules.open_chain('cable_randomSingleContainer', 'container.chain', folded=0))
	cable_randomSingleL = modules.add_clone_cable(f'randomSingleL', NUM_MODES, value=1.0, min_value= -1.0, max_value = 1.0, mode="Random", use_container=False)
	cable_randomSingleR = modules.add_clone_cable(f'randomSingleR', NUM_MODES, value=1.0, min_value= -1.0, max_value = 1.0, mode="Random", use_container=False)
	cable_randomSingleIntensityL = modules.add_clone_cable(f'randomSingleIntensityL', NUM_MODES, value=1.0, min_value= 0.0, max_value = 1.0, mode="Fixed", use_container=True)
	cable_randomSingleIntensityR = modules.add_clone_cable(f'randomSingleIntensityR', NUM_MODES, value=1.0, min_value= 0.0, max_value = 1.0, mode="Fixed", use_container=True)
	nodes.append(cable_randomSingleL)	
	nodes.append(cable_randomSingleR)	
	nodes.append(cable_randomSingleIntensityL)
	nodes.append(cable_randomSingleIntensityR)
	nodes.append(modules.close_chain('cable_randomSingleContainer'))

	# End Params
	nodes.append(modules.close_chain('global_params'))

	# Begin Oscillators
	if STEREO_INSTRUMENT:
		nodes.append(modules.open_chain("multiChannel", "container.multi", folded=1))

	# Left Channel
	nodes.append(modules.open_chain("chainL", "container.chain", folded=1))

	# Cloner Object
	nodes.append(modules.open_cloner('clonerL'))

	# Left Channel (Or Center if !Stereo)
	for i in range(NUM_MODES):
		nodes.append([f'<!-- Begin Clone Child -->'])
		nodes.append([f'<Node ID="sineL_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
		nodes.append([f'<Nodes>'])

		# Need these declared...
		
		ahdsr_pitch = modules.add_AHDSR(f'sineL_{i}_ahdsrPitch', 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 

		pma_randomSingle = modules.add_pma(f'sineL_{i}_pmaRandomSingle', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)
		pma_randomGlobal = modules.add_pma(f'sineL_{i}_pmaRandomGlobal', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)

		pma_combineA = modules.add_pma(f'sineL_{i}_pmaCombineA', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)
		pma_combineB = modules.add_pma(f'sineL_{i}_pmaCombineB', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)

		# Need to normalize ratio input
		pma_normalizer = modules.add_pma(f'sineL_{i}_pma_normalizer', 1.0, 1.0, 0.0, scaled=False)
		pma_output = modules.add_pma(f'sineL_{i}_pma_output', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0, add_max=1.0, value_max=100.0)
		sine = modules.add_sine(f'sineL_{i}', 1.0)

		nodes.append(modules.open_chain(f'sineL_{i}_pitchSplit', 'container.split', folded=True))
		nodes.append(ahdsr_pitch)		
		nodes.append(pma_randomGlobal)
		nodes.append(pma_randomSingle)		
		nodes.append(modules.close_chain(f'sineL_{i}_pitchSplit'))
		nodes.append(pma_combineA)
		nodes.append(pma_combineB)		
		nodes.append(pma_normalizer)
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
			modules.connect_module(cable_pitchFalloffIntensityL, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'AttackLevel')	
			modules.connect_module(cable_pitchFalloffDecayL, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'Decay')							
			modules.connect_module(cable_randomGlobalL, '<ModulationTargets>', f'sineL_{i}_pmaRandomGlobal', 'Value')
			modules.connect_module(cable_randomGlobalIntensityL, 'ModulationTargets>', f'sineL_{i}_pmaRandomGlobal', 'Multiply')
			modules.connect_module(cable_randomSingleL, '<ModulationTargets>', f'sineL_{i}_pmaRandomSingle', 'Value')
			modules.connect_module(cable_randomSingleIntensityL, 'ModulationTargets>', f'sineL_{i}_pmaRandomSingle', 'Multiply')
			modules.connect_module(sliderpack_ratiosL, '<ModulationTargets>', f'sineL_{i}_pma_normalizer', 'Value')

		# Stack Pitch Modulation
		modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineL_{i}_pmaCombineA', 'Value')
		modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineL_{i}_pmaCombineA', 'Add')

		modules.connect_module(pma_combineA, '<ModulationTargets>', f'sineL_{i}_pmaCombineB', 'Value')
		modules.connect_module(pma_randomSingle, '<ModulationTargets>', f'sineL_{i}_pmaCombineB', 'Add')

		modules.connect_module(pma_combineB, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Add')

		modules.connect_module(pma_normalizer, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Value')		

		modules.connect_module(pma_output, '<ModulationTargets>', f'sineL_{i}', 'Freq Ratio')

	nodes.append(modules.close_cloner("clonerL", NUM_MODES))
	
	if STEREO_INSTRUMENT:
		nodes.append(modules.add_jpanner("jpanLeft", -1.0))

	nodes.append(modules.close_chain("chainL"))

	# RIGHT SIDE
	if STEREO_INSTRUMENT:
		# Right Channel
		nodes.append(modules.open_chain("chainR", "container.chain", folded=1))

		# Cloner Object
		nodes.append(modules.open_cloner('clonerR'))

		# Right Channel
		for i in range(NUM_MODES):
			nodes.append([f'<!-- Begin Clone Child -->'])
			nodes.append([f'<Node ID="sineR_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
			nodes.append([f'<Nodes>'])

			# Need these declared...
			
			ahdsr_pitch = modules.add_AHDSR(f'sineR_{i}_ahdsrPitch', 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 

			pma_randomSingle = modules.add_pma(f'sineR_{i}_pmaRandomSingle', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)
			pma_randomGlobal = modules.add_pma(f'sineR_{i}_pmaRandomGlobal', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)

			pma_combineA = modules.add_pma(f'sineR_{i}_pmaCombineA', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)
			pma_combineB = modules.add_pma(f'sineR_{i}_pmaCombineB', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)

			# Need to normalize ratio input
			pma_normalizer = modules.add_pma(f'sineR_{i}_pma_normalizer', 1.0, 1.0, 0.0, scaled=False)
			pma_output = modules.add_pma(f'sineR_{i}_pma_output', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0, add_max=1.0, value_max=100.0)
			sine = modules.add_sine(f'sineR_{i}', 1.0)

			nodes.append(modules.open_chain(f'sineR_{i}_pitchSplit', 'container.split', folded=True))
			nodes.append(ahdsr_pitch)		
			nodes.append(pma_randomGlobal)
			nodes.append(pma_randomSingle)		
			nodes.append(modules.close_chain(f'sineR_{i}_pitchSplit'))
			nodes.append(pma_combineA)
			nodes.append(pma_combineB)		
			nodes.append(pma_normalizer)
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
				modules.connect_module(cable_pitchFalloffIntensityR, '<ModulationTargets>', f'sineR_{i}_ahdsrPitch', 'AttackLevel')	
				modules.connect_module(cable_pitchFalloffDecayR, '<ModulationTargets>', f'sineR_{i}_ahdsrPitch', 'Decay')							
				modules.connect_module(cable_randomGlobalR, '<ModulationTargets>', f'sineR_{i}_pmaRandomGlobal', 'Value')
				modules.connect_module(cable_randomGlobalIntensityR, 'ModulationTargets>', f'sineR_{i}_pmaRandomGlobal', 'Multiply')
				modules.connect_module(cable_randomSingleR, '<ModulationTargets>', f'sineR_{i}_pmaRandomSingle', 'Value')
				modules.connect_module(cable_randomSingleIntensityR, 'ModulationTargets>', f'sineR_{i}_pmaRandomSingle', 'Multiply')
				#modules.connect_module(sliderpack_ratiosR, '<ModulationTargets>', f'sineR_{i}_pma_normalizer', 'Value')



			# Stack Pitch Modulation
			'''
			modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineR_{i}_pmaCombineA', 'Value')
			modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineR_{i}_pmaCombineA', 'Add')

			modules.connect_module(pma_combineA, '<ModulationTargets>', f'sineR_{i}_pmaCombineB', 'Value')
			modules.connect_module(pma_randomSingle, '<ModulationTargets>', f'sineR_{i}_pmaCombineB', 'Add')

			modules.connect_module(pma_combineB, '<ModulationTargets>', f'sineR_{i}_pma_output', 'Add')

			modules.connect_module(pma_normalizer, '<ModulationTargets>', f'sineR_{i}_pma_output', 'Value')		

			modules.connect_module(pma_output, '<ModulationTargets>', f'sineR_{i}', 'Freq Ratio')
			'''

		nodes.append(modules.close_cloner("clonerR", NUM_MODES))

		nodes.append(modules.add_jpanner("jpanRight", 1.0))
		nodes.append(modules.close_chain("chainR"))
		nodes.append(modules.close_chain("multiChannel"))

	# Stiffness

	nodes.append(modules.open_chain("tanhSplit", "container.split", folded=1))
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

	# Connect Global Parameters		
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'cable_pitchFalloffIntensityL', 'Value')	
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'cable_pitchFalloffDecayL', 'Value')	
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalBang', 'cable_randomGlobalL', 'Value')	
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalIntensity', 'cable_randomGlobalIntensityL', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomSingleIntensity', 'cable_randomSingleIntensityL', 'Value')

	if STEREO_INSTRUMENT:
		modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'cable_pitchFalloffIntensityR', 'Value')
		modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'cable_pitchFalloffDecayR', 'Value')
		modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalBang', 'cable_randomGlobalR', 'Value')	
		modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalIntensity', 'cable_randomGlobalIntensityR', 'Value')
		modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomSingleIntensity', 'cable_randomSingleIntensityR', 'Value')

	modules.connect_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 'ahdsrFilter', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhDry', 'Gain')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhWet', 'Gain')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffnessType', 'stiffnessSwitch', 'Type')
	modules.connect_parameter(NETWORK_PARAMS, 'filterStaticFrequency', 'lowPass', 'Frequency')

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

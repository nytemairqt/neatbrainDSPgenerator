#networkbuilder

string = '<?xml version="1.0" encoding="UTF-8"?>'
PATH = 'D:/Documents/HISE/neatbraintestingSCRIPTNODE/DspNetworks/Networks'

import modules
from hyperparameters import *

file = open(f'{PATH}/neatbrain.xml', 'w')

# TO DO

# add pan nodes when stereo 
# setup velocity -> pitchAHDSR attack level or something
# add filter cutoff static parameter
# pitch bend (global pitch mod i think)

# Instantiate XML Doc

NETWORK_START = []
NETWORK_PARAMS = []
NETWORK_END = []

NETWORK_START.append('<?xml version="1.0" encoding="UTF-8"?>')
NETWORK_START.append('<Network ID="testnew" AllowPolyphonic="1" Version="0.0.0">')
NETWORK_START.append('<Node FactoryPath="container.chain" ID="testnew" Bypassed="0" ShowParameters="1">')
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

modules.create_parameter(NETWORK_PARAMS, 'stiffness', 0.0, 1.0, 0.01, 0.0)
modules.create_parameter(NETWORK_PARAMS, 'pitchVelocity', 0.0, 1.0, 0.01, 0.0)
modules.create_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 0.0, 1.0, 0.01, PITCH_FALLOFF_INTENSITY)
modules.create_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 20, 20000, 1, PITCH_FALLOFF_DECAY)
modules.create_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 20, 20000, 1, FILTER_FALLOFF_DECAY)

# Connections


if __name__=="__main__":
	# be careful using restoreState() on the scriptnode synth

	# Instantiate Nodes

	ahdsr_pitch = modules.add_AHDSR("ahdsrPitch", 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 
	ahdsr_filter = modules.add_AHDSR("ahdsrFilter", 5.0, 1.0, FILTER_FALLOFF_DECAY, 0.0, 50) # A AL D S R 

	nodes = []
	pmas = []

	#nodes.append(ahdsr_gain)
	nodes.append(ahdsr_filter)
	nodes.append(ahdsr_pitch)

	if STEREO_INSTRUMENT:
		nodes.append(modules.open_chain("multiChannel", "container.multi", folded=1))

	# Left Channel
	nodes.append(modules.open_chain("sines_splitterL", "container.split"))

	# Build Sine Wave Chains
	for i in range(NUM_MODES):
		# Create Modules
		nodes.append(modules.open_chain(f'sineL_{i}_chain', 'container.chain', folded=1))
		bang_input = modules.add_bang(f'sineL_{i}_bangInput', 0.1) # connect to parameter "Random Strength"
		cable = modules.add_cable_expr(f'sineL_{i}_cable', 'Math.random() * input')
		bang_output = modules.add_bang(f'sineL_{i}_bangOutput', 1.0)
		pma_ahdsrStrength = modules.add_pma(f'sineL_{i}_pma_ahdsrStrength', 1.0, PITCH_FALLOFF_INTENSITY, 1.0) # Connect Multiply to "Strength" Param, connect Value to AHDSR_Pitch
		pma_ahdsr = modules.add_pma(f'sineL_{i}_pma_ahdsr', 1.0, 1.0, 1.0) # Connect Value to "Modes{i}", connect Add to previous PMA
		pma_random = modules.add_pma(f'sineL_{i}_pma_random', 1.0, 1.0, 0.0)
		pma_randomGlobal = modules.add_pma(f'sineL_{i}_pma_randomGlobal', 1.0, 1.0, 0.0)
		pma_output = modules.add_pma(f'sineL_{i}_pma_output', RATIOS_L[i], 1.0, 0.0)
		nodes.append(bang_input)
		nodes.append(cable)
		nodes.append(bang_output)
		nodes.append(pma_ahdsrStrength) 
		nodes.append(pma_ahdsr) 
		nodes.append(pma_random)
		nodes.append(pma_randomGlobal)
		nodes.append(pma_output)
		nodes.append(modules.add_sine(f'sineL_{i}', 1.0 + (1.0*i)))
		nodes.append(modules.add_gain(f'sineL_{i}_gain', False))
		nodes.append(modules.close_chain(f'sineL_{i}_chain'))
		# Connect Modules
		modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', f'sineL_{i}_pma_ahdsrStrength', 'Multiply')
		modules.connect_module(bang_input, '<ModulationTargets>', f'sineL_{i}_cable', 'Value')
		modules.connect_module(cable, '<ModulationTargets>', f'sineL_{i}_bangOutput', 'Value')
		modules.connect_module(bang_output, '<ModulationTargets>', f'sineL_{i}_pma_random', 'Add')
		modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineL_{i}_pma_ahdsrStrength', 'Value')
		modules.connect_module(pma_ahdsrStrength, '<ModulationTargets>', f'sineL_{i}_pma_ahdsr', 'Add')
		modules.connect_module(pma_ahdsr, '<ModulationTargets>', f'sineL_{i}_pma_random', 'Value')
		modules.connect_module(pma_random, '<ModulationTargets>', f'sineL_{i}_pma_randomGlobal', 'Value')
		modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Add')
		modules.connect_module(pma_output, '<ModulationTargets>', f'sineL_{i}', 'Freq Ratio')		
	nodes.append(modules.close_chain("sines_splitterL"))

	if STEREO_INSTRUMENT:
		# Right Channel
		nodes.append(modules.open_chain("sines_splitterR", "container.split"))

		# Build Sine Wave Chains
		for i in range(NUM_MODES):
			# Create Modules
			nodes.append(modules.open_chain(f'sineR_{i}_chain', 'container.chain'))
			bang_input = modules.add_bang(f'sineR_{i}_bangInput', 0.1)
			cable = modules.add_cable_expr(f'sineR_{i}_cable', 'Math.random() * input')
			bang_output = modules.add_bang(f'sineR_{i}_bangOutput', 1.0)
			pma_ahdsrStrength = modules.add_pma(f'sineR_{i}_pma_ahdsrStrength', 1.0, PITCH_FALLOFF_INTENSITY, 1.0) # Connect Multiply to "Strength" Param, connect Value to AHDSR_Pitch
			pma_ahdsr = modules.add_pma(f'sineR_{i}_pma_ahdsr', 1.0, 1.0, 1.0) # Connect Value to "Modes{i}", connect Add to previous PMA
			pma_random = modules.add_pma(f'sineR_{i}_pma_random', 1.0, 1.0, 0.0)
			pma_randomGlobal = modules.add_pma(f'sineR_{i}_pma_randomGlobal', 1.0, 1.0, 0.0)
			pma_output = modules.add_pma(f'sineR_{i}_pma_output', RATIOS_R[i], 1.0, 0.0)
			nodes.append(bang_input)
			nodes.append(cable)
			nodes.append(bang_output)
			nodes.append(pma_ahdsrStrength) 
			nodes.append(pma_ahdsr) 
			nodes.append(pma_random)
			nodes.append(pma_randomGlobal)
			nodes.append(pma_output)
			nodes.append(modules.add_sine(f'sineR_{i}', 1.0 + (1.0*i)))
			nodes.append(modules.add_gain(f'sineR_{i}_gain', False))
			nodes.append(modules.close_chain(f'sineR_{i}_chain'))
			# Connect Modules
			modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', f'sineR_{i}_pma_ahdsrStrength', 'Multiply')
			modules.connect_module(bang_input, '<ModulationTargets>', f'sineR_{i}_cable', 'Value')
			modules.connect_module(cable, '<ModulationTargets>', f'sineR_{i}_bangOutput', 'Value')
			modules.connect_module(bang_output, '<ModulationTargets>', f'sineR_{i}_pma_random', 'Add')
			modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineR_{i}_pma_ahdsrStrength', 'Value')
			modules.connect_module(pma_ahdsrStrength, '<ModulationTargets>', f'sineR_{i}_pma_ahdsr', 'Add')
			modules.connect_module(pma_ahdsr, '<ModulationTargets>', f'sineR_{i}_pma_random', 'Value')
			modules.connect_module(pma_random, '<ModulationTargets>', f'sineR_{i}_pma_randomGlobal', 'Value')
			modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineR_{i}_pma_output', 'Add')
			modules.connect_module(pma_output, '<ModulationTargets>', f'sineR_{i}', 'Freq Ratio')	
		nodes.append(modules.close_chain("sines_splitterR"))
		nodes.append(modules.close_chain("multiChannel"))

	# Tanh

	nodes.append(modules.open_chain("tanhSplit", "container.split"))
	nodes.append(modules.open_chain("tanhOff", "container.chain"))
	nodes.append(modules.add_gain("tanhDry", invert=True))
	nodes.append(modules.close_chain("tanhOff"))
	nodes.append(modules.open_chain("tanhOn", "container.chain"))
	nodes.append(modules.add_expr("tanh", 'input + Math.tanh(input)'))
	nodes.append(modules.add_expr("abs", 'input + Math.abs(input)'))
	nodes.append(modules.add_gain("tanhWet", invert=False))
	nodes.append(modules.close_chain("tanhOn"))
	nodes.append(modules.close_chain("tanhSplit"))

	# Filters
	nodes.append(modules.add_filter('lowPass', 2000))
	nodes.append(modules.add_filter('ahdsrFilter', 4000))
	modules.connect_module(ahdsr_filter, '<!-- CV -->', 'ahdsrFilter', 'Frequency')	

	# Connect Global Parameters	
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'ahdsrPitch', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 'ahdsrFilter', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhDry', 'Gain')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhWet', 'Gain')

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
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

# random global: bang -> cable.expr -> bang out -> pma_global_random(add) using Fixed cable
# random global strength = Fixed Cable value 
# this way we don't need any external modulators

# finish connecting stuff
# IMPORTANT: uncomment out filters, tanh etc etc
# for static parameters, just change the Value of the sliderpack (and make sure sliders are 1.0!)
# set Random to go between -1 and 1

# by exposing the sliderpacks to the end user, we could create presets that sound like different instruments...
# just save the ratios as a json object or array 
# velocity PITCH
# velocity FILTER
# velocity AMPLITUDE (maybe)
# pitch bend (global pitch mod i think)

# normalize = (x[i] - min(x)) / (max(x) - min(x))
# denorm = z[i] * (max(x) - min(x)) + min(x)
# normalize values first
# in scriptnode, plug the sliderpack into a chain
# using Mul, Sub, Div and Add nodes
# plug min(x) and max(x) into network as parameters and those control the operators
# not too bad

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

	#ahdsr_pitch = modules.add_AHDSR("ahdsrPitch", 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 
	ahdsr_filter = modules.add_AHDSR("ahdsrFilter", 5.0, 1.0, FILTER_FALLOFF_DECAY, 0.0, 50) # A AL D S R 
	sliderpack_ratiosL = modules.add_clone_sliderpack("ratiosL", NUM_MODES)
	sliderpack_ratiosR = modules.add_clone_sliderpack("ratiosR", NUM_MODES)


	#sliderpack_stiffness = modules.add_clone_sliderpack("sliderpackStiffness", 1)


	#nodes.append(ahdsr_gain)
	nodes.append(modules.open_chain('ahdsrs', 'container.split', folded=1))
	nodes.append(ahdsr_filter)
	#nodes.append(ahdsr_pitch)
	nodes.append(modules.close_chain('ahdsrs'))
	nodes.append(modules.open_chain('ratioChains', 'container.split'))
	nodes.append(sliderpack_ratiosL)
	nodes.append(sliderpack_ratiosR)
	nodes.append(modules.close_chain('ratioChains'))

	# Parameter Nodes for Clones

	nodes.append(modules.open_chain('global_params', 'container.split', folded=0))

	cable_pitchFalloffIntensity = modules.add_clone_cable(f'pitchFalloffIntensity', NUM_MODES, mode="Fixed")		
	cable_pitchFalloffDecay = modules.add_clone_cable(f'pitchFalloffDecay', NUM_MODES, mode="Fixed")	
	cable_pitchRandomIntensity = modules.add_clone_cable(f'pitchRandomIntensity', NUM_MODES, mode="Fixed")	
	nodes.append(cable_pitchFalloffIntensity)
	nodes.append(cable_pitchFalloffDecay)
	nodes.append(cable_pitchRandomIntensity)

	# Random Global



	chain_randomGlobal = modules.open_chain('chain_randomGlobal', 'container.chain', folded=1)
	pitchMod_randomGlobal = modules.add_pitch_mod('pitchMod_randomGlobal', index=0)

	nodes.append(chain_randomGlobal)
	nodes.append(pitchMod_randomGlobal)




	
	#nodes.append(modules.add_clone_cable(f'pitchFalloffIntensity', NUM_MODES, mode="Fixed"))
	#nodes.append(modules.add_clone_cable(f'pitchFalloffDecay', NUM_MODES, mode="Fixed"))
	#nodes.append(modules.add_clone_cable(f'pitchRandomIntensity', NUM_MODES, mode="Fixed"))
	#add_clone_cable(name, num_clones, mode="Fixed")
	#nodes.append(modules.add_clone_sliderpack(f'ahdsrPitch', NUM_MODES))
	#nodes.append(modules.add_clone_sliderpack(f'pitchFalloffIntensity', NUM_MODES))
	#nodes.append(modules.add_clone_sliderpack(f'pitchFalloffDecay', NUM_MODES))
	#nodes.append(modules.add_clone_sliderpack(f'pitchRandomIntensity', NUM_MODES))
	nodes.append(modules.close_chain('chain_randomGlobal'))

	# Random Single
	cable_randomSingle = modules.add_clone_cable(f'randomSingle', NUM_MODES, value=1.0, mode="Random", use_container=False)

	nodes.append(cable_randomSingle)
	

	nodes.append(modules.close_chain('global_params'))

	# Begin Oscillators

	if STEREO_INSTRUMENT:
		nodes.append(modules.open_chain("multiChannel", "container.multi", folded=1))

	# Left Channel
	nodes.append(modules.open_chain("chainL", "container.chain"))

	# Cloner Object

	nodes.append(modules.open_cloner('clonerL'))

	# Clone Chain

	# ===============================BACKUP================================
	''' 
	for i in range(NUM_MODES):
		nodes.append([f'<!-- Begin Clone Child -->'])
		nodes.append([f'<Node ID="clone_child" FactoryPath="container.chain" Bypassed="0">'])
		nodes.append([f'<Nodes>'])
		nodes.append(modules.open_chain(f'sineL_chain', 'container.chain', folded=1))
		bang_input = modules.add_bang(f'sineL_bangInput', 0.1) # connect to parameter "Random Strength"
		cable = modules.add_cable_expr(f'sineL_cable', 'Math.random() * input')
		bang_output = modules.add_bang(f'sineL_bangOutput', 1.0)
		pma_ahdsrStrength = modules.add_pma(f'sineL_pma_ahdsrStrength', 1.0, PITCH_FALLOFF_INTENSITY, 1.0) # Connect Multiply to "Strength" Param, connect Value to AHDSR_Pitch
		pma_ahdsr = modules.add_pma(f'sineL_pma_ahdsr', 1.0, 1.0, 1.0) # Connect Value to "Modes{i}", connect Add to previous PMA
		pma_random = modules.add_pma(f'sineL_pma_random', 1.0, 1.0, 0.0)
		pma_randomGlobal = modules.add_pma(f'sineL_pma_randomGlobal', 1.0, 1.0, 0.0)
		pma_output = modules.add_pma(f'sineL_pma_output', 1.0, 1.0, 0.0)
		nodes.append(bang_input)
		nodes.append(cable)
		nodes.append(bang_output)
		nodes.append(pma_ahdsrStrength) 
		nodes.append(pma_ahdsr) 
		nodes.append(pma_random)
		nodes.append(pma_randomGlobal)
		nodes.append(pma_output)
		nodes.append(modules.add_sine(f'sineL', 1.0))
		nodes.append(modules.close_chain(f'sineL_chain'))
		nodes.append([f'</Nodes>'])
		nodes.append([f'<Parameters/>'])
		nodes.append([f'</Node>'])
		nodes.append([f'<!-- End Clone Child -->'])
	'''
	# =======================================================================

	for i in range(NUM_MODES):
		nodes.append([f'<!-- Begin Clone Child -->'])
		nodes.append([f'<Node ID="sineL_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
		nodes.append([f'<Nodes>'])

		# Need these declared...
		ahdsr_pitch = modules.add_AHDSR(f"sineL_{i}_ahdsrPitch", 5.0, 1.0, PITCH_FALLOFF_DECAY, 0.0, 50) # A AL D S R 


		# add a single random modulator to the Synth
		# use pitch_mod for Global Random
		# CLONE CABLE has a RANDOM mode for individual random, plug randomIntensity into the Value as a global multiplier

		#pma_ahdsrStrength = modules.add_pma(f'sineL_{i}_pma_ahdsrStrength', 1.0, 1.0, 0.0) # Connect Multiply to "Strength" Param, connect Value to AHDSR_Pitch
		#pma_ahdsr = modules.add_pma(f'sineL_{i}_pma_ahdsr', 1.0, 1.0, 0.0) # Connect Value to "Modes{i}", connect Add to previous PMA
		#pma_ahdsr = modules.add_pma(f'sineL_{i}_pma_ahdsr', 1.0, 1.0, 0.0, scaled=True, value_max=1.0, multiply_max=1.0, add_max=1.0)
		pma_random = modules.add_pma(f'sineL_{i}_pma_random', 1.0, 1.0, 0.0, value_max=1.0, multiply_max=1.0, add_max=1.0)
		pma_randomGlobal = modules.add_pma(f'sineL_{i}_pma_randomGlobal', 1.0, 1.0, 0.0, value_max=1.0, multiply_max=1.0, add_max=1.0)
		denormalizer_open = modules.open_chain(f'sineL_{i}_denormalizer', 'container.chain', folded=0)

		# USE CONTROL.MINMAX YOU CLOWN
		# create sliderpack, give it the ratios for values
		# connect sliderpack to this
		minmax = modules.add_minmax(f'sineL_{i}_minmax', denorm_ratios["min_ratio_L"], denorm_ratios["max_ratio_L"])
		# connect minmax to base pitch (pma output:value i think)


		# sliderpackvalue * (max(x) - min(x)) + min(x)
		# cable.expr -> 1-value min(x):value || INVERTED MIN
		# pma -> max(x):value, 1-min(x):add || max(x) - min(x) (invert MIN to use PMA)
		# pma -> slider:value, :add


		denormalizer_close = modules.close_chain(f'sineL_{i}_denormalizer')
		pma_ratio_scalar = modules.add_pma(f'sineL_{i}_pma_ratioScalar', 1.0, 1.0, 0.0, scaled=True)
		pma_output = modules.add_pma(f'sineL_{i}_pma_output', 1.0, 1.0, 0.0)
		sine = modules.add_sine(f'sineL_{i}', 1.0)

		nodes.append(ahdsr_pitch)		
		#nodes.append(pma_ahdsrStrength)
		#nodes.append(pma_ahdsr)
		nodes.append(pma_random)
		nodes.append(pma_randomGlobal)
		nodes.append(pma_ratio_scalar)
		nodes.append(denormalizer_open)
		nodes.append(minmax)
		nodes.append(denormalizer_close)
		nodes.append(pma_output)
		nodes.append(sine)

		nodes.append([f'</Nodes>'])
		nodes.append([f'<Parameters/>'])
		nodes.append([f'</Node>']) # Manually Close
		nodes.append([f'<!-- End Clone Child -->'])

		# Connect Everything

		
		#modules.connect_module(pma_ratio_scalar, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Value')

		# AHDSR
		#modules.connect_parameter(nodes, 'sliderpack_pitchFalloffIntensity', f'sineL_{i}_ahdsrPitch', 'AttackLevel', check_for_node=True)		
		#modules.connect_parameter(nodes, 'sliderpack_pitchFalloffDecay', f'sineL_{i}_ahdsrPitch', 'Decay', check_for_node=True)		
		#modules.connect_parameter(nodes, 'cable_pitchFalloffIntensity', f'sineL_{i}_ahdsrPitch', 'AttackLevel', check_for_node=True)		

		# ============================
		# ONLY CONNECT THE FIRST CLONE
		# ============================
		if i == 0:
			#modules.connect_module(sliderpack_ratiosL, '<ModulationTargets>', f'sineL_{i}_pma_ratioScalar', 'Value')
			modules.connect_module(cable_pitchFalloffIntensity, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'AttackLevel')	
			modules.connect_module(cable_pitchFalloffDecay, '<ModulationTargets>', f'sineL_{i}_ahdsrPitch', 'Decay')
			modules.connect_module(cable_pitchRandomIntensity, '<ModulationTargets>', f'sineL_{i}_bangInput', 'Value')
			modules.connect_module(cable_randomSingle, '<ModulationTargets>', f'sineL_{i}_pma_random', 'Add')	
									
		modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineL_{i}_pma_random', 'Value')
		#modules.connect_module(ahdsr_pitch, '<!-- CV -->', 'sliderpack_ahdsrPitch', 'Value')	
		#modules.connect_parameter(nodes, 'sliderpack_ahdsrPitch', f'sineL_{i}_pma_ahdsr', 'Value', check_for_node=True)		
		#modules.connect_parameter(nodes, 'sliderpack_pitchFalloffIntensity', f'sineL_{i}_pma_ahdsr', 'Multiply', check_for_node=True)		
		
		#modules.connect_module(pma_ahdsrStrength, '<ModulationTargets>', f'sineL_{i}_pma_ahdsr', 'Value')

		# Random Single
		#modules.connect_parameter(nodes, 'sliderpack_pitchRandomIntensity', f'sineL_{i}_bangInput', 'Value', check_for_node=True)				
		#modules.connect_module(bang_input, '<ModulationTargets>', f'sineL_{i}_cable', 'Value')
		#modules.connect_module(cable, '<ModulationTargets>', f'sineL_{i}_bangOutput', 'Value')
		#modules.connect_module(cable_randomSingle, '<ModulationTargets>', f'sineL_{i}_pma_random', 'Add')	
		
		modules.connect_module(minmax, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Value')
		modules.connect_module(pma_random, '<ModulationTargets>', f'sineL_{i}_pma_randomGlobal', 'Value')		
		modules.connect_module(pma_randomGlobal, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Add')
		modules.connect_module(pma_output, '<ModulationTargets>', f'sineL_{i}', 'Freq Ratio')

		#modules.connect_module(ahdsr_pitch, '<!-- CV -->', f'sineL_{i}_pma_ahdsrStrength', 'Value') # connect to ahdsr

	nodes.append(modules.close_cloner("clonerL", NUM_MODES))



	#nodes.append(modules.open_chain("sines_splitterL", "container.split"))

	'''

	# OLD STATIC METHOD
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
	'''		
	#nodes.append(modules.close_chain("sines_splitterL"))
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

		#nodes.append(modules.open_chain("sines_splitterR", "container.split"))

		'''
	

		# OLD STATIC METHOD

		# Build Sine Wave Chains
		for i in range(NUM_MODES):
			# Create Modules
			nodes.append(modules.open_chain(f'sineR_{i}_chain', 'container.chain', folded=1))
			bang_input = modules.add_bang(f'sineR_{i}_bangInput', 0.1)
			cable = modules.add_cable_expr(f'sineR_{i}_cable', 'Math.random() * input')
			bang_output = modules.add_bang(f'sineR_{i}_bangOutput', 1.0)
			pma_ahdsrStrength = modules.add_pma(f'sineR_{i}_pma_ahdsrStrength', 1.0, PITCH_FALLOFF_INTENSITY, 1.0)
			pma_ahdsr = modules.add_pma(f'sineR_{i}_pma_ahdsr', 1.0, 1.0, 1.0)
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
		'''		
		#nodes.append(modules.close_chain("sines_splitterR"))
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

	#modules.connect_module(sliderpack_ratiosL, '<ModulationTargets>', 'sineL_pma_output', 'Value')
	#modules.connect_module(sliderpack_ratiosR, '<ModulationTargets>', 'sineR_pma_output', 'Value')
	#modules.connect_parameter(NETWORK_PARAMS, '<ModulationTargets>', )

	# Connect Global Parameters		
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'cable_pitchFalloffIntensity', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'cable_pitchFalloffDecay', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomIntensity', 'cable_randomSingle', 'Value')
	#modules.connect_parameter(NETWORK_PARAMS, '')
	#cable_randomSingle
	#modules.connect_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 'ahdsrFilter', 'Decay')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhDry', 'Gain')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffness', 'tanhWet', 'Gain')
	#modules.connect_parameter(NETWORK_PARAMS, 'stiffnessType', 'stiffnessSwitch', 'Type')
	#modules.connect_parameter(NETWORK_PARAMS, 'filterStaticFrequency', 'lowPass', 'Frequency')


	# Connect Bang Inputs to Pitch

	#for i in range(NUM_MODES):
	#	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomIntensity', f'sineL_{i}_bangInput', 'Value')

	#if STEREO_INSTRUMENT:
	#	for i in range(NUM_MODES):
	#		modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomIntensity', f'sineR_{i}_bangInput', 'Value')

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

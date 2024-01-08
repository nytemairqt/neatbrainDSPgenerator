# Import

string = '<?xml version="1.0" encoding="UTF-8"?>'
PATH = 'D:/Documents/HISE/neatbraininstrument/DspNetworks/Networks'

import modules
from hyperparameters import *

file = open(f'{PATH}/NEATBrain_Achromic.xml', 'w')

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

parameters = {	
	'pitchFalloffIntensity' : [0.0, 1.0, 0.01, 0.05],
	'pitchFalloffDecay' : [0, 40000, 1, 2200],	
	'pitchDriftIntensity' : [0.0, 0.2, 0.01, 0.1],
	'pitchRandomGlobalBang' : [-1.0, 1.0, 0.01, 0.1],
	'pitchRandomGlobalIntensity' : [0.0, 1.0, 0.01, 0.04],
	'pitchRandomSingleIntensity' : [0.0, 1.0, 0.01, 0.01],
	'filterFalloffIntensity' : [0.0, 1.0, 0.01, 1.0],
	'filterFalloffDecay' : [0, 40000, 1, 5000],
	'filterStaticFrequency' : [100, 20000, 1, 3000],	
	'stiffnessIntensity' : [0.0, 1.0, 0.01, 0.0],
	'stiffnessType' : [0.0, 1.0, 1.0, 0.0],
}

for param in reversed(parameters):
	modules.create_parameter(NETWORK_PARAMS, param, parameters[param][0], parameters[param][1], parameters[param][2], parameters[param][3])

for ratio in denorm_ratios:
	modules.create_parameter(NETWORK_PARAMS, ratio, denorm_ratios[ratio], denorm_ratios[ratio], 0.01, denorm_ratios[ratio])	
	
# Connections

if __name__=="__main__":

	# Instantiate Nodes

	nodes = []
	
	ahdsr_filter = modules.add_AHDSR("ahdsrFilter", 5.0, 1.0, 5000, 0.0, 50) # A AL D S R 
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

	# Pitch Mod Stack Left

	nodes.append(modules.open_chain('pitchModL', 'container.chain', folded=0))
	midi_VelocityL = modules.add_midi(f'midiVelocityL', 'Velocity')
	pma_VelocityL = modules.add_pma(f'pmaVelocityL', 1.0, 1.0, 0.0, scaled=False)
	ahdsr_PitchFalloffL = modules.add_AHDSR(f'ahdsrVelocityL', 5.0, 1.0, 2000, 0.0, 50)
	pma_randomGlobalL = modules.add_pma(f'pmaRandomGlobalL', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, value_max=1.0) # Bang -> Value, Intensity -> Mult	
	pma_CombineAL = modules.add_pma(f'pmaCombineAL', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0) # AHDSR & RandomGlobal
	midi_PitchBendL = modules.add_midi_cc('pitchBendL', 128.0)
	bipolar_PitchBendL = modules.add_bipolar(f'bipolarPitchBendL', value_min=-1.0, value_max=1.0, scale_min=0.0, scale_max=1.0, scale=1.0)
	pma_CombineBL = modules.add_pma(f'pmaCombineBL', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0) # CombineA & PitchBend
	cable_pitchModL = modules.add_clone_cable(f'cable_pitchModL', NUM_MODES, mode="Fixed", use_container=False, min_value=-1.0)

	nodes.append(midi_VelocityL)
	nodes.append(pma_VelocityL)
	nodes.append(ahdsr_PitchFalloffL)
	nodes.append(pma_randomGlobalL)
	nodes.append(pma_CombineAL)
	nodes.append(midi_PitchBendL)
	nodes.append(bipolar_PitchBendL)
	nodes.append(pma_CombineBL)
	nodes.append(cable_pitchModL)
	nodes.append(modules.close_chain('pitchModL'))

	# Connect Params
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'pmaVelocityL', 'Multiply')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'ahdsrVelocityL', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalBang', 'pmaRandomGlobalL', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalIntensity', 'pmaRandomGlobalL', 'Multiply')

	# Connect Modules
	modules.connect_module(midi_VelocityL, '<ModulationTargets>', 'pmaVelocityL', 'Value')
	modules.connect_module(pma_VelocityL, '<ModulationTargets>', 'ahdsrVelocityL', 'AttackLevel')
	modules.connect_module(ahdsr_PitchFalloffL, '<!-- CV -->', 'pmaCombineAL', 'Value')
	modules.connect_module(pma_randomGlobalL, '<ModulationTargets>', 'pmaCombineAL', 'Add')
	modules.connect_module(pma_CombineAL, '<ModulationTargets>', 'pmaCombineBL', 'Value')
	modules.connect_module(midi_PitchBendL, '<ModulationTargets>', 'bipolarPitchBendL', 'Value')
	modules.connect_module(bipolar_PitchBendL, '<ModulationTargets>', 'pmaCombineBL', 'Add')
	modules.connect_module(pma_CombineBL, '<ModulationTargets>', 'cable_pitchModL', 'Value')

	# Pitch Mod Stack Right

	nodes.append(modules.open_chain('pitchModR', 'container.chain', folded=1))
	midi_VelocityR = modules.add_midi(f'midiVelocityR', 'Velocity')
	pma_VelocityR = modules.add_pma(f'pmaVelocityR', 1.0, 1.0, 0.0, scaled=False)
	ahdsr_PitchFalloffR = modules.add_AHDSR(f'ahdsrVelocityR', 5.0, 1.0, 2000, 0.0, 50)
	pma_randomGlobalR = modules.add_pma(f'pmaRandomGlobalR', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, value_max=1.0) # Bang -> Value, Intensity -> Mult	
	pma_CombineAR = modules.add_pma(f'pmaCombineAR', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0) # AHDSR & RandomGlobal
	midi_PitchBendR = modules.add_midi_cc('pitchBendR', 128.0)
	bipolar_PitchBendR = modules.add_bipolar(f'bipolarPitchBendR', value_min=-1.0, value_max=1.0, scale_min=0.0, scale_max=1.0, scale=1.0)
	pma_CombineBR = modules.add_pma(f'pmaCombineBR', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0) # CombineA & PitchBend
	cable_pitchModR = modules.add_clone_cable(f'cable_pitchModR', NUM_MODES, mode="Fixed", use_container=False, min_value=-1.0)

	nodes.append(midi_VelocityR)
	nodes.append(pma_VelocityR)
	nodes.append(ahdsr_PitchFalloffR)
	nodes.append(pma_randomGlobalR)
	nodes.append(pma_CombineAR)
	nodes.append(midi_PitchBendR)
	nodes.append(bipolar_PitchBendR)
	nodes.append(pma_CombineBR)
	nodes.append(cable_pitchModR)
	nodes.append(modules.close_chain('pitchModR'))

	# Connect Params
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffIntensity', 'pmaVelocityR', 'Multiply')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchFalloffDecay', 'ahdsrVelocityR', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalBang', 'pmaRandomGlobalR', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomGlobalIntensity', 'pmaRandomGlobalR', 'Multiply')

	# Connect Modules
	modules.connect_module(midi_VelocityR, '<ModulationTargets>', 'pmaVelocityR', 'Value')
	modules.connect_module(pma_VelocityR, '<ModulationTargets>', 'ahdsrVelocityR', 'AttackLevel')
	modules.connect_module(ahdsr_PitchFalloffR, '<!-- CV -->', 'pmaCombineAR', 'Value')
	modules.connect_module(pma_randomGlobalR, '<ModulationTargets>', 'pmaCombineAR', 'Add')
	modules.connect_module(pma_CombineAR, '<ModulationTargets>', 'pmaCombineBR', 'Value')
	modules.connect_module(midi_PitchBendR, '<ModulationTargets>', 'bipolarPitchBendR', 'Value')
	modules.connect_module(bipolar_PitchBendR, '<ModulationTargets>', 'pmaCombineBR', 'Add')
	modules.connect_module(pma_CombineBR, '<ModulationTargets>', 'cable_pitchModR', 'Value')

	# Random Single
	nodes.append(modules.open_chain('cable_randomSingleContainer', 'container.chain', folded=0))
	cable_randomSingleL = modules.add_clone_cable(f'cable_randomSingleL', NUM_MODES, value=1.0, min_value=-1.0, max_value=1.0, mode="Random", use_container=False)
	cable_randomSingleR = modules.add_clone_cable(f'cable_randomSingleR', NUM_MODES, value=1.0, min_value=-1.0, max_value=1.0, mode="Random", use_container=False)
	cable_randomSingleIntensityL = modules.add_clone_cable(f'cable_randomSingleIntensityL', NUM_MODES, value=1.0, min_value=0.0, max_value = 1.0, mode="Fixed", use_container=True)
	cable_randomSingleIntensityR = modules.add_clone_cable(f'cable_randomSingleIntensityR', NUM_MODES, value=1.0, min_value=0.0, max_value = 1.0, mode="Fixed", use_container=True)
	nodes.append(cable_randomSingleL)	
	nodes.append(cable_randomSingleR)	
	nodes.append(cable_randomSingleIntensityL)
	nodes.append(cable_randomSingleIntensityR)
	nodes.append(modules.close_chain('cable_randomSingleContainer'))

	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomSingleIntensity', 'cable_randomSingleIntensityL', 'Value')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchRandomSingleIntensity', 'cable_randomSingleIntensityR', 'Value')

	# LFO Drift Left
	nodes.append(modules.open_chain('chainLFODriftL', 'container.chain'))
	
	nodes.append(modules.open_chain('noMidiLFODriftL', 'container.no_midi'))
	nodes.append(modules.open_chain('modchainLFODriftL', 'container.modchain'))

	lfoDriftL = modules.add_sine(f'lfoDriftL', 1.0, frequency=0.35, min_freq=0.3, max_freq=5.0)
	sig2modDriftL = modules.add_sig2mod(f'sig2modDriftL')
	peakDriftL = modules.add_peak(f'peakDriftL')
	bipolarDriftL = modules.add_bipolar(f'bipolarDriftL', scale_max=0.2, scale=0.2)

	nodes.append(lfoDriftL)
	nodes.append(sig2modDriftL)
	nodes.append(peakDriftL)
	nodes.append(bipolarDriftL)

	nodes.append(modules.close_chain('modchainLFODriftL'))
	nodes.append(modules.close_chain('noMidiLFODriftL'))
		
	cable_lfoDriftL = modules.add_clone_cable(f'cable_lfoDriftL', NUM_MODES, value=1.0, min_value=0.0, max_value=1.0, mode="Fixed", use_container=True)

	nodes.append(cable_lfoDriftL)
	nodes.append(modules.close_chain('chainLFODriftL'))

	modules.connect_module(peakDriftL, '<ModulationTargets>', 'bipolarDriftL', 'Value')
	modules.connect_module(bipolarDriftL, '<ModulationTargets>', 'cable_lfoDriftL', 'Value')

	# LFO Drift Right
	nodes.append(modules.open_chain('chainLFODriftR', 'container.chain', folded=1))
	
	nodes.append(modules.open_chain('noMidiLFODriftR', 'container.no_midi'))
	nodes.append(modules.open_chain('modchainLFODriftR', 'container.modchain'))

	lfoDriftR = modules.add_sine(f'lfoDriftR', 1.0, frequency=0.32, min_freq=0.3, max_freq=5.0, phase=.35)
	sig2modDriftR = modules.add_sig2mod(f'sig2modDriftR')
	peakDriftR = modules.add_peak(f'peakDriftR')
	bipolarDriftR = modules.add_bipolar(f'bipolarDriftR', scale_max=0.2, scale=0.2)

	nodes.append(lfoDriftR)
	nodes.append(sig2modDriftR)
	nodes.append(peakDriftR)
	nodes.append(bipolarDriftR)

	nodes.append(modules.close_chain('modchainLFODriftR'))
	nodes.append(modules.close_chain('noMidiLFODriftR'))
		
	cable_lfoDriftR = modules.add_clone_cable(f'cable_lfoDriftR', NUM_MODES, value=1.0, min_value=-0.2, max_value=0.2, mode="Fixed", use_container=True)
	nodes.append(cable_lfoDriftR)
	nodes.append(modules.close_chain('chainLFODriftR'))

	modules.connect_module(peakDriftR, '<ModulationTargets>', 'bipolarDriftR', 'Value')
	modules.connect_module(bipolarDriftR, '<ModulationTargets>', 'cable_lfoDriftR', 'Value')


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

		# Instantiate Modules

		pma_randomSingle = modules.add_pma(f'sineL_{i}_pmaRandomSingle', 1.0, 1.0, 0.0, scaled=False, value_max=1.0, add_min=-1.0, add_max=1.0)
		pma_drift = modules.add_pma(f'sineL_{i}_pma_drift', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0, add_max=1.0)
		pma_pitchStack = modules.add_pma(f'sineL_{i}_pmaPitchStack', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0)		
		pma_normalizer = modules.add_pma(f'sineL_{i}_pma_normalizer', 1.0, 1.0, 0.0, scaled=False)
		pma_output = modules.add_pma(f'sineL_{i}_pma_output', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0, add_max=1.0, value_max=100.0)
		sine = modules.add_sine(f'sineL_{i}', 1.0)

		nodes.append(pma_randomSingle)		
		nodes.append(pma_drift)
		nodes.append(pma_pitchStack)		
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
			modules.connect_module(cable_pitchModL, '<ModulationTargets>', f'sineL_{i}_pmaPitchStack', 'Value')
			modules.connect_module(cable_randomSingleL, '<ModulationTargets>', f'sineL_{i}_pmaRandomSingle', 'Value')
			modules.connect_module(cable_randomSingleIntensityL, '<ModulationTargets>', f'sineL_{i}_pmaRandomSingle', 'Multiply')
			modules.connect_module(cable_lfoDriftL, '<ModulationTargets>', f'sineL_{i}_pma_drift', 'Add') 
			modules.connect_module(sliderpack_ratiosL, '<ModulationTargets>', f'sineL_{i}_pma_normalizer', 'Value')

		# Connect Pitch Modulation
		modules.connect_module(pma_randomSingle, '<ModulationTargets>', f'sineL_{i}_pma_drift', 'Value')
		modules.connect_module(pma_drift, '<ModulationTargets>', f'sineL_{i}_pmaPitchStack', 'Add')
		modules.connect_module(pma_normalizer, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Value')	
		modules.connect_module(pma_pitchStack, '<ModulationTargets>', f'sineL_{i}_pma_output', 'Add')
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

		# Left Channel (Or Center if !Stereo)
		for i in range(NUM_MODES):
			nodes.append([f'<!-- Begin Clone Child -->'])
			nodes.append([f'<Node ID="sineR_{i}_chain" FactoryPath="container.chain" Bypassed="0">'])
			nodes.append([f'<Nodes>'])

			# Instantiate Modules

			pma_randomSingle = modules.add_pma(f'sineR_{i}_pmaRandomSingle', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, value_max=1.0, add_min=-1.0, add_max=1.0)
			pma_drift = modules.add_pma(f'sineR_{i}_pma_drift', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0)
			pma_pitchStack = modules.add_pma(f'sineR_{i}_pmaPitchStack', 1.0, 1.0, 0.0, scaled=False, value_min=-1.0, add_min=-1.0)			
			pma_normalizer = modules.add_pma(f'sineR_{i}_pma_normalizer', 1.0, 1.0, 0.0, scaled=False)
			pma_output = modules.add_pma(f'sineR_{i}_pma_output', 1.0, 1.0, 0.0, scaled=False, add_min=-1.0, add_max=1.0, value_max=100.0)
			sine = modules.add_sine(f'sineR_{i}', 1.0)

			nodes.append(pma_randomSingle)	
			nodes.append(pma_drift)	
			nodes.append(pma_pitchStack)
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
				modules.connect_module(cable_pitchModR, '<ModulationTargets>', f'sineR_{i}_pmaPitchStack', 'Value')
				modules.connect_module(cable_randomSingleR, '<ModulationTargets>', f'sineR_{i}_pmaRandomSingle', 'Value')
				modules.connect_module(cable_randomSingleIntensityR, '<ModulationTargets>', f'sineR_{i}_pmaRandomSingle', 'Multiply')
				modules.connect_module(cable_lfoDriftR, '<ModulationTargets>', f'sineR_{i}_pma_drift', 'Add') 
				modules.connect_module(sliderpack_ratiosR, '<ModulationTargets>', f'sineR_{i}_pma_normalizer', 'Value')

			# Connect Pitch Modulation
			modules.connect_module(pma_randomSingle, '<ModulationTargets>', f'sineR_{i}_pma_drift', 'Value')
			modules.connect_module(pma_drift, '<ModulationTargets>', f'sineR_{i}_pmaPitchStack', 'Add')
			modules.connect_module(pma_normalizer, '<ModulationTargets>', f'sineR_{i}_pma_output', 'Value')	
			modules.connect_module(pma_pitchStack, '<ModulationTargets>', f'sineR_{i}_pma_output', 'Add')
			modules.connect_module(pma_output, '<ModulationTargets>', f'sineR_{i}', 'Freq Ratio')

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

	modules.connect_parameter(NETWORK_PARAMS, 'pitchDriftIntensity', 'bipolarDriftL', 'Scale')
	modules.connect_parameter(NETWORK_PARAMS, 'pitchDriftIntensity', 'bipolarDriftR', 'Scale')
	modules.connect_parameter(NETWORK_PARAMS, 'filterFalloffDecay', 'ahdsrFilter', 'Decay')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffnessIntensity', 'tanhDry', 'Gain')
	modules.connect_parameter(NETWORK_PARAMS, 'stiffnessIntensity', 'tanhWet', 'Gain')
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


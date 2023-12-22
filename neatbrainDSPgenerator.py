#networkbuilder

string = '<?xml version="1.0" encoding="UTF-8"?>'
PATH = 'D:/Documents/HISE/neatbraintestingSCRIPTNODE/DspNetworks/Networks'

file = open(f'{PATH}/neatbrain.xml', 'w')

# load modes & hyperparams as a JSON object
# get loris to extract the amplitude envelopes

# Hyperparameters

NUM_MODES = 5

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

# Individual Nodes

def open_chain(name, chain_type):
	chain = []
	chain.append(f'<!-- Begin Chain {name} -->')
	chain.append(f'<Node ID="{name}" FactoryPath="{chain_type}" Bypassed="0">') # container.chain, container.split
	chain.append(f'<Nodes>')
	return chain

def close_chain(name):
	chain = []
	chain.append(f'</Nodes>')
	chain.append(f'<Parameters/>')
	chain.append(f'</Node>')
	chain.append(f'<!-- End Chain {name} -->')
	return chain

def add_sine(name, freq_ratio):
	# maybe test adjusting the min/max limits for inter-modal randomness?
	# alternatively just use noteOn and set the ratios as parameters...
	sine = []
	sine.append(f'<!-- Oscillator {name} -->')
	sine.append(f'<Node ID="{name}" FactoryPath="core.oscillator" Bypassed="0">')
	sine.append(f'<ComplexData>')
	sine.append(f'<DisplayBuffers>')
	sine.append(f'<DisplayBuffer Index="-1"/>')
	sine.append(f'</DisplayBuffers>')
	sine.append(f'</ComplexData>')
	sine.append(f'<Parameters>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="4.0" StepSize="1.0" ID="Mode" Automated="1"/>')
	sine.append(f'<Parameter MinValue="20.0" MaxValue="20000.0" StepSize="0.1000000014901161" SkewFactor="0.2299045622348785" ID="Frequency" Value="220.0"/>')
	sine.append(f'<Parameter MinValue="1.0" MaxValue="30.0" StepSize="1.0" ID="Freq Ratio" Value="{freq_ratio}"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Gate" Value="1.0"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Phase" Value="0.0"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Gain" Value="1.0"/>')
	sine.append(f'</Parameters>')
	sine.append(f'</Node>')
	sine.append(f'<!-- End Oscillator -->')
	return sine

def add_AHDSR(name, attack, attack_level, decay, sustain, release):
	ahdsr = []
	ahdsr.append(f'<!-- AHDSR {name} -->')
	ahdsr.append(f'<Node ID="{name}" FactoryPath="envelope.ahdsr" Bypassed="0">')
	ahdsr.append(f'<Properties>')
	ahdsr.append(f'<Property ID="NumParameters" Value="2"/>')
	ahdsr.append(f'</Properties>')
	ahdsr.append(f'<SwitchTargets>')
	ahdsr.append(f'<SwitchTarget>')
	ahdsr.append(f'<Connections> <!-- CV -->')
	ahdsr.append(f'</Connections>')
	ahdsr.append(f'</SwitchTarget>')
	ahdsr.append(f'<SwitchTarget>')
	ahdsr.append(f'<Connections> <!-- GT -->')
	ahdsr.append(f'</Connections>')
	ahdsr.append(f'</SwitchTarget>')
	ahdsr.append(f'</SwitchTargets>')
	ahdsr.append(f'<ComplexData>')
	ahdsr.append(f'<DisplayBuffers>')
	ahdsr.append(f'<DisplayBuffer Index="-1" EmbeddedData=""/>')
	ahdsr.append(f'</DisplayBuffers>')
	ahdsr.append(f'</ComplexData>')
	ahdsr.append(f'<Parameters>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="10000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Attack" Value="{attack}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="AttackLevel" Value="{attack_level}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="10000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Hold" Value="20.0"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="40000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Decay" Value="{decay}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Sustain" Value="{sustain}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="30000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Release" Value="{release}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="AttackCurve" Value="0.5"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Retrigger" Value="0.0"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Gate" Value="0.0"/>')
	ahdsr.append(f'</Parameters>')
	ahdsr.append(f'</Node> <!-- End AHDSR -->')
	return ahdsr 

def connect_AHDSR(ahdsr, connection_id, node_id, parameter_id):
	for idx, line in enumerate(ahdsr):
		if connection_id in line:
			ahdsr.insert(idx+1, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')

def create_parameter(name, min_value, max_value, step_size, value, node_id, parameter_id):
	for idx, line in enumerate(NETWORK_PARAMS):
		if '<Parameters>' in line:
			NETWORK_PARAMS.insert(idx+1, f'<Parameter ID="{name}" MinValue="{min_value}" MaxValue="{max_value}" StepSize="{step_size}" Value="{value}">')
			NETWORK_PARAMS.insert(idx+2, f'<Connections>')
			NETWORK_PARAMS.insert(idx+3, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')
			NETWORK_PARAMS.insert(idx+4, f'</Connections>')			
			NETWORK_PARAMS.insert(idx+5, f'</Parameter>')

def add_filter(name, frequency):
	lowpassFilter = []
	lowpassFilter.append(f'<Node ID="{name}" FactoryPath="filters.one_pole" Bypassed="0">')
	lowpassFilter.append(f'<ComplexData>')
	lowpassFilter.append(f'<Filters>')
	lowpassFilter.append(f'<Filter Index="-1" EmbeddedData=""/>')
	lowpassFilter.append(f'</Filters>')
	lowpassFilter.append(f'</ComplexData>')
	lowpassFilter.append(f'<Parameters>')
	lowpassFilter.append(f'<Parameter MinValue="20.0" MaxValue="20000.0" SkewFactor="0.2299045622348785"')
	lowpassFilter.append(f'ID="Frequency" Value="{frequency}"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.300000011920929" MaxValue="9.899999618530273" SkewFactor="0.2647178173065186"')
	lowpassFilter.append(f'ID="Q" Value="1.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="-18.0" MaxValue="18.0" ID="Gain" Value="0.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" SkewFactor="0.3010300099849701"')
	lowpassFilter.append(f'ID="Smoothing" Value="0.009999999776482582"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Mode" Value="0.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Enabled" Value="1.0"/>')
	lowpassFilter.append(f'</Parameters>')
	lowpassFilter.append(f'</Node>')
	return lowpassFilter

def add_voice_manager(name):
	voice_manager = []
	voice_manager.append(f'<Node ID="{name}" FactoryPath="envelope.voice_manager" Bypassed="0">')
	voice_manager.append(f'<Parameters>')
	voice_manager.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Kill Voice" Automated="1"/>')
	voice_manager.append(f'</Parameters>')
	voice_manager.append(f'</Node>')
	return voice_manager


# Connections


if __name__=="__main__":
	# be careful using restoreState() on the scriptnode synth

	# Instantiate Nodes

	ahdsr_gain = add_AHDSR("ahdsrGain", 5.0, 1.0, 18000, 0.0, 50) # A AL D S R 
	ahdsr_pitch = add_AHDSR("ahdsrPitch", 5.0, 1.0, 18000, 0.0, 50) # A AL D S R 
	ahdsr_filter = add_AHDSR("ahdsrFilter", 5.0, 1.0, 4000, 0.0, 50) # A AL D S R 
	multi = open_chain("multiChannel", "container.multi")
	multi_close = close_chain("multiChannel")
	split_L = open_chain("sines_splitterL", "container.split")
	split_R = open_chain("sines_splitterR", "container.split")
	split_close_L = close_chain("sines_splitterL")
	split_close_R = close_chain("sines_splitterR")
	voice_manager = add_voice_manager('voiceManager')
	lowpassFilter = add_filter('lowPass', 2000)

	nodes = []

	nodes.append(ahdsr_gain)
	nodes.append(ahdsr_filter)
	nodes.append(ahdsr_pitch)
	nodes.append(multi)

	# Left Channel
	nodes.append(split_L)

	# Build Sine Wave Chains
	for i in range(NUM_MODES):
		#nodes.append(open_chain(f'sineL_{i}_chain', 'container.chain'))
		nodes.append(add_sine(f'sineL_{i}', 1.0 + (1.0*i))) # ratios[i]
		#nodes.append(close_chain(f'sineL_{i}_chain'))
		connect_AHDSR(ahdsr_gain, '<!-- CV -->', f'sineL_{i}', 'Gain')
	nodes.append(split_close_L)

	# Right Channel
	nodes.append(split_R)

	# Build Sine Wave Chains
	for i in range(NUM_MODES):
		#nodes.append(open_chain(f'sineR_{i}_chain', 'container.chain'))
		nodes.append(add_sine(f'sineR_{i}', 1.0 + (1.0*i))) # ratios[i]
		#nodes.append(close_chain(f'sineR_{i}_chain'))
		connect_AHDSR(ahdsr_gain, '<!-- CV -->', f'sineR_{i}', 'Gain')
	nodes.append(split_close_R)

	nodes.append(multi_close)
	nodes.append(lowpassFilter)
	nodes.append(voice_manager)
	connect_AHDSR(ahdsr_gain, '<!-- GT -->', 'voiceManager', 'Kill Voice')
	connect_AHDSR(ahdsr_gain, '<!-- CV -->', 'lowPass', 'Frequency')

	# Create & Connect Parameters

	create_parameter('derek', 0.0, 1.0, 0.1, 0.66, 'lowPass', 'Smoothing')

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
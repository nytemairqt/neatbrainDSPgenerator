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
NETWORK_PARAMS.append('<Parameters/>') # no params to start...

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
	sine.append(f'<Parameter MinValue="1.0" MaxValue="16.0" StepSize="1.0" ID="Freq Ratio" Value="{freq_ratio}"/>')
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

def add_filter(name, frequency):
	return None

def add_voice_manager(name):
	voice_manager = []
	voice_manager.append(f'<Node ID="{name}" FactoryPath="envelope.voice_manager" Bypassed="0">')
	voice_manager.append(f'<Parameters>')
	voice_manager.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Kill Voice" Automated="1"/>')
	voice_manager.append(f'</Parameters>')
	voice_manager.append(f'</Node>')
	return voice_manager
	

def connect_cable(name1, name2):
	return None




# Connections


if __name__=="__main__":
	# use Scriptnode Voice Killer on ScriptFX Module
	# be careful when using SVK & restoreState on the scriptnode synth
	# add a voice_manager node 
	# connect AHDSR Gate Output to the VoiceKill socket of voice manager node
	ahdsr_gain = add_AHDSR("ahdsrGain", 5.0, 1.0, 18000, 0.0, 50)
	ahdsr_pitch = add_AHDSR("ahdsrPitch", 5.0, 1.0, 18000, 0.0, 50)
	split = open_chain("sines_splitter", "container.split")
	split_close = close_chain("sines_splitter")
	voice_manager = add_voice_manager('voiceManager')

	nodes = []

	nodes.append(ahdsr_gain)

	nodes.append(ahdsr_pitch)
	nodes.append(split)
	for i in range(NUM_MODES):
		nodes.append(open_chain(f'sine_{i}_chain', 'container.chain'))
		nodes.append(add_sine(f'sine_{i}', 1.0 + (1.0*i))) # ratios[i]
		nodes.append(close_chain(f'sine_{i}_chain'))
		connect_AHDSR(ahdsr_gain, '<!-- CV -->', f'sine_{i}', 'Gain')
		#chain = open_chain(f'sine_{i}_chain', 'container.chain')
		#sine = add_sine(f'sine_{i}', 1.0 + (1.0*i)) # ratios[i]
		# add other modules here
		#chain_end = close_chain(f'sine_{i}_chain')
		#nodes.append(chain)
		#nodes.append(sine)
		#nodes.append(chain_end)
	nodes.append(split_close)
	nodes.append(voice_manager)
	connect_AHDSR(ahdsr_gain, '<!-- GT -->', 'voiceManager', 'Kill Voice')

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
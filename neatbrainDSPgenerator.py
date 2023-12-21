#networkbuilder

string = '<?xml version="1.0" encoding="UTF-8"?>'
PATH = 'D:/Documents/HISE/neatbraintestingSCRIPTNODE/DspNetworks/Networks'

file = open(f'{PATH}/demofile.xml', 'w')

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

def open_chain(name):
	chain = []
	chain.append(f'<!-- Begin Chain {name} -->')
	chain.append(f'<Node ID="{name}" FactoryPath="container.split" Bypassed="0">')
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
	mode = []
	mode.append(f'<!-- Oscillator {name} -->')
	mode.append(f'<Node ID="{name}" FactoryPath="core.oscillator" Bypassed="0">')
	mode.append(f'<ComplexData>')
	mode.append(f'<DisplayBuffers>')
	mode.append(f'<DisplayBuffer Index="-1"/>')
	mode.append(f'</DisplayBuffers>')
	mode.append(f'</ComplexData>')
	mode.append(f'<Parameters>')
	mode.append(f'<Parameter MinValue="0.0" MaxValue="4.0" StepSize="1.0" ID="Mode" Automated="1"/>')
	mode.append(f'<Parameter MinValue="20.0" MaxValue="20000.0" StepSize="0.1000000014901161" SkewFactor="0.2299045622348785" ID="Frequency" Value="220.0"/>')
	mode.append(f'<Parameter MinValue="1.0" MaxValue="16.0" StepSize="1.0" ID="Freq Ratio" Value="{freq_ratio}"/>')
	mode.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Gate" Value="1.0"/>')
	mode.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Phase" Value="0.0"/>')
	mode.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Gain" Value="1.0"/>')
	mode.append(f'</Parameters>')
	mode.append(f'</Node>')
	mode.append(f'<!-- End Oscillator -->')
	return mode

def add_AHDSR(name, attack, decay, sustain, release):
	return None 

def add_filter(name, frequency):
	return None

def connect_cable(name1, name2):
	return None


# Connections


if __name__=="__main__":

	split = open_chain("sines_splitter")
	split_close = close_chain("sines_splitter")

	nodes = []

	nodes.append(split)
	for i in range(5):
		sine = add_sine(f'sine_{i}', 1.0 + (1.0*i))
		nodes.append(sine)
	nodes.append(split_close)

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
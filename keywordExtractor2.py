import yake

text = "PROJECT SUMMARY The major open question in microtubule motor research is to determine how cargo-scale motor behavior is regulated (at the molecular scale) to orchestrate control of a cell's spatial organization (on the scale of 10-100 microns), simultaneously for all of motor- driven intracellular traffic. This involves the microtubule associated protein Tau, the hallmark of Tauopathy diseases. Challenges arise because of the combinatorial complexity of Tau variants and the multi-scale nature of the question – two challenges for which computational modeling is particularly well suited to confront. In Aim 1, we will develop a model to simulate motor-MAP kinetics and how these lead to cargo transport. We hypothesize that a microtubule adorned with MAPs and other molecules can selectively influence cargo localization depending on the cargo's size and mechanical deformability. This selectivity can be understood in terms of the MAP's size, mechanical properties and abundance, which together provide a traffic coding system that is mis- regulated in disease. We will develop a computational model and simulate motor transport at the cargo-scale to explore specificity and multiplexing by MT-cargo spacing control. A key missing parameter is the motor's attachment rates, which have been so far too technically challenging to measure directly and will therefore require a novel experimental-theoretical assay. We will then simulate motor transport in a 1-dimensional array of microtubules to identify cargo-scale parameters that sensitively lead to cell-scale localization, using known spatial heterogeneity of, e.g., Tau across axons. In Aim 2, we will explore the spacing-based aspect of motor modulators. We hypothesize that many transport-regulating molecules operate in part by tuning the spacing (mean and variance of distance) between the microtubule and cargo. Spacing-based regulation endows the system with control properties not present in other modes of regulation. We will develop an optical tweezer-based assay to quantify the modulation of transport parameters by tuning MT-cargo spacing, and a simulation-based inference method to measure spacing for arbitrary MAPs. We will specifically work to understand the regulatory mechanism of highly-structured molecules such as Dynactin and Rabs, and highly-disordered molecules such as Tau and MAP2. In Aim 3, we will explore the effects of the cargo's and cell's local rheology. We hypothesize that both the internal dynamics of surface- bound molecules on the cargo, and the cell's local rheology influence transport properties. This provides the system with a natural cargo sorting mechanism. Using our simulation, we will quantify the influence of the cargo's internal viscosity (low for vesicular cargo, intermediate for lipid droplets, and high for rigid cargo like RNA) and how this interacts with the viscoelasticity of the cytoplasm."

kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw in keywords:
	print(kw)



language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, 
	dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)
import pke

def getKeywords(text):

    verbose = 0

    # initialize keyphrase extraction model, here TopicRank
    extractor = pke.unsupervised.TopicRank()

    

    # load the content of the document, here document is expected to be in raw
    # format (i.e. a simple text file) and preprocessing is carried out using spacy
    extractor.load_document(input=text, language='en')

    # loading a document populates the extractor.sentences list
    # let's have a look at the pre-processed text

    if verbose:
        # for each sentence in the document
        for i, sentence in enumerate(extractor.sentences):
            
            # print out the sentence id, its tokens, its stems and the corresponding Part-of-Speech tags
            print("sentence {}:".format(i))
            print(" - words: {} ...".format(' '.join(sentence.words[:5])))
            print(" - stems: {} ...".format(' '.join(sentence.stems[:5])))
            print(" - PoS: {} ...".format(' '.join(sentence.pos[:5])))


    # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
    # and adjectives (i.e. `(Noun|Adj)*`)
    extractor.candidate_selection()

    # identifying keyphrase candidates populates the extractor.candidates dictionary
    # let's have a look at the keyphrase candidates

    if verbose:
        # for each keyphrase candidate
        for i, candidate in enumerate(extractor.candidates):
            
            # print out the candidate id, its stemmed form 
            print("candidate {}: {} (stemmed form)".format(i, candidate))
            
            # print out the surface forms of the candidate
            print(" - surface forms:", [ " ".join(u) for u in extractor.candidates[candidate].surface_forms])
            
            # print out the corresponding offsets
            print(" - offsets:", extractor.candidates[candidate].offsets)
            
            # print out the corresponding sentence ids
            print(" - sentence_ids:", extractor.candidates[candidate].sentence_ids)
            
            # print out the corresponding PoS patterns
            print(" - pos_patterns:", extractor.candidates[candidate].pos_patterns)

    # candidate weighting, in the case of TopicRank: using a random walk algorithm
    extractor.candidate_weighting()

    if verbose:
        # let's have a look at the topics

        # for each topic of the document
        for i, topic in enumerate(extractor.topics):
            
            # print out the topic id and the candidates it groups together
            print("topic {}: {} ".format(i, ';'.join(topic)))

    # N-best selection, keyphrases contains the 10 highest scored candidates as
    # (keyphrase, score) tuples
        #keyphrases = extractor.get_n_best(n=10)

    # print the n-highest (10) scored candidates
    for (keyphrase, score) in extractor.get_n_best(n=35, stemming=True):
        #print(keyphrase, score)
        print(keyphrase)

if __name__ == "__main__":

    text = '''
    Functional assessment of iMGLs reveals that they secrete cytokines in response to inflammatory stimuli, migrate and undergo calcium transients, and robustly phagocytose CNS substrates. iMGLs were used to examine the effects of Aβ fibrils and brain-derived tau oligomers on AD-related gene expression and to interrogate mechanisms involved in synaptic pruning. Furthermore, iMGLs transplanted into transgenic mice and human brain organoids resemble microglia in vivo. Together, these findings demonstrate that iMGLs can be used to study microglial function, providing important new insight into human neurological disease.", '3D organoids", "AD-GWAS", "Alzheimer's disease", "Beta-amyloid", "Tau", "cell models of disease", "induced pluripotent stem cells", "microglia", "mouse transplantation", "neurodegenerative diseases', 'Activated entomopathogenic nematode infective juveniles release lethal venom proteins.', 'Entomopathogenic nematodes (EPNs) are unique parasites due to their symbiosis with entomopathogenic bacteria and their ability to kill insect hosts quickly after infection. It is widely believed that EPNs rely on their bacterial partners for killing hosts. Here we disproved this theory by demonstrating that the in vitro activated infective juveniles (IJs) of Steinernema carpocapsae (a well-studied EPN species) release venom proteins that are lethal to several insects including Drosophila melanogaster. We confirmed that the in vitro activation is a good approximation of the in vivo process by comparing the transcriptomes of individual in vitro and in vivo activated IJs. We further analyzed the transcriptomes of non-activated and activated IJs and revealed a dramatic shift in gene expression during IJ activation. We also analyzed the venom proteome using mass spectrometry. Among the 472 venom proteins, proteases and protease inhibitors are especially abundant, and toxin-related proteins such as Shk domain-containing proteins and fatty acid- and retinol-binding proteins are also detected, which are potential candidates for suppressing the host immune system. Many of the venom proteins have conserved orthologs in vertebrate-parasitic nematodes and are differentially expressed during IJ activation, suggesting conserved functions in nematode parasitism. In summary, our findings strongly support a new model that S. carpocapsae and likely other Steinernema EPNs have a more active role in contributing to the pathogenicity of the nematode-bacterium complex than simply relying on their symbiotic bacteria. Furthermore, we propose that EPNs are a good model system for investigating vertebrate- and human-parasitic nematodes, especially regarding the function of excretory/secretory products.', '3D organoids", "AD-GWAS", "Alzheimer’s disease", "Beta-amyloid", "Tau", "cell models of disease", "induced pluripotent stem cells", "microglia", "mouse transplantation", "neurodegenerative diseases', 'Dynamic Gene Regulatory Networks of Human Myeloid Differentiation.', 'The reconstruction of gene regulatory networks underlying cell differentiation from high-throughput gene expression and chromatin data remains a challenge. Here, we derive dynamic gene regulatory networks for human myeloid differentiation using a 5-day time series of RNA-seq and ATAC-seq data. We profile HL-60 promyelocytes differentiating into macrophages, neutrophils, monocytes, and monocyte-derived macrophages. We find a rapid response in the expression of key transcription factors and lineage markers that only regulate a subset of their targets at a given time, which is followed by chromatin accessibility changes that occur later along with further gene expression changes. We observe differences between promyelocyte- and monocyte-derived macrophages at both the transcriptional and chromatin landscape level, despite using the same differentiation stimulus, which suggest that the path taken by cells in the differentiation landscape defines their end cell state. More generally, our approach of combining neighboring time points and replicates to achieve greater sequencing depth can efficiently infer footprint-based regulatory networks from long series data.', 'ATAC-seq", "RNA-seq", "footprinting", "gene regulatory network", "macrophage", "monocyte", "myeloid differentiation", "neutrophil", "open chromatin', 'NRSF-dependent epigenetic mechanisms contribute to programming of stress-sensitive neurons by neonatal experience, promoting resilience.', 'Resilience to stress-related emotional disorders is governed in part by early-life experiences. Here we demonstrate experience-dependent re-programming of stress-sensitive hypothalamic neurons, which takes place through modification of neuronal gene expression via epigenetic mechanisms. Specifically, we found that augmented maternal care reduced glutamatergic synapses onto stress-sensitive hypothalamic neurons and repressed expression of the stress-responsive gene, Crh. In hypothalamus in vitro, reduced glutamatergic neurotransmission recapitulated the repressive effects of augmented maternal care on Crh, and this required recruitment of the transcriptional repressor repressor element-1 silencing transcription factor/neuron restrictive silencing factor (NRSF). Increased NRSF binding to chromatin was accompanied by sequential repressive epigenetic changes which outlasted NRSF binding. chromatin immunoprecipitation-seq analyses of NRSF targets identified gene networks that, in addition to Crh, likely contributed to the augmented care-induced phenotype, including diminished depression-like and anxiety-like behaviors. Together, we believe these findings provide the first causal link between enriched neonatal experience, synaptic refinement and induction of epigenetic processes within specific neurons. They uncover a novel mechanistic pathway from neonatal environment to emotional resilience.', 'ATAC-seq", "RNA-seq", "footprinting", "gene regulatory network", "macrophage", "monocyte", "myeloid differentiation", "neutrophil", "open chromatin', 'Regeneration of fat cells from myofibroblasts during wound healing.', 'Although regeneration through the reprogramming of one cell lineage to another occurs in fish and amphibians, it has not been observed in mammals. We discovered in the mouse that during wound healing, adipocytes regenerate from myofibroblasts, a cell type thought to be differentiated and nonadipogenic. Myofibroblast reprogramming required neogenic hair follicles, which triggered bone morphogenetic protein (BMP) signaling and then activation of adipocyte transcription factors expressed during development. Overexpression of the BMP antagonist Noggin in hair follicles or deletion of the BMP receptor in myofibroblasts prevented adipocyte formation. Adipocytes formed from human keloid fibroblasts either when treated with BMP or when placed with human hair follicles in vitro', 'ATAC-seq", "RNA-seq", "footprinting", "gene regulatory network", "macrophage", "monocyte", "myeloid differentiation", "neutrophil", "open chromatin
    '''

    getKeywords(text)
import numpy
import json
import pybel
import os
import pandas.rpy.common as com

class MolResolver(object):
    """
    This class manages retrieving molecules from the in-house SD file 
    by the CAS number that is annotated in DoOR.
    """
    def __init__(self):
        gabler2013path = os.path.realpath(os.path.join(
            os.path.dirname(__file__) , 'DODO_molecule_database.sdf'))
        all_mols_generator = pybel.readfile("mol",gabler2013path)
        all_mols = []
        for m in all_mols_generator:
            if 'Name' in m.data.keys():
                title = m.data['Name']
            else:
                title = m.data['Smiles']
            m.title = title
            all_mols.append(m)
        
        self.CdId2mol = {m.data['CdId']:m for m in all_mols} 
        door2idpath = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                                                        'DODO_door2id.json'))
        self.door2id = json.load(open(door2idpath,'r'))
        
    def resolve_cas(self, cas):
        """
        returns a pybel molecule corresponding to the CAS number.
        """
        CdId = self.door2id[cas]
        if len(CdId) > 1:
            raise(Warning("CAS %s maps to more than one CdIds " + 
                            "(probably stereoisomers): %s")%(cas, CdId))
        if len(CdId) < 1:
            raise(Warning("CAS %s doens't map to a molecule."%cas))
        else: 
            mol = self.CdId2mol[CdId[0]]
        return mol

    def resolve_cas_SVG(self, cas):
        """
        retrieve the molecule with the given CAS, but return an SVG for 
        visualization in the notebook.
        """
        mol = self.resolve_cas(cas)
        return mol.write("svg", opt={'C':None, 'u':None})
        

class HallemFromDoOR(object):
    """
    Retrieve the Hallem data directly from DoOR.
    """
    def __init__(self):
        com.importr('DoOR.data', lib_loc=os.path.dirname(__file__))
        self.hallems = ['Or2a', 'Or7a', 'Or9a', 'Or10a', 'Or19a', 'Or22a', 
                        'Or23a', 'Or33b', 'Or35a', 'Or43a', 'Or43b', 'Or47a', 
                        'Or47b', 'Or49b', 'Or59b', 'Or65a', 'Or67a', 'Or67c', 
                        'Or82a', 'Or85a', 'Or85b', 'Or85f', 'Or88a', 'Or98a']

    def load_data(self):
        """
        retrieve the data from the DoOR database, but only those odorants that 
        have been measured in Hallem et al., 2006.
        """
        self.hallemresponses = {}
        measured = None
        for OR in self.hallems:
            dataframe = com.load_data(OR)
            dataframe_hallemonly = dataframe[['Hallem.2006.EN','CAS', 'Name']]
            responses = numpy.array(dataframe[['Hallem.2006.EN']], dtype=float)
            cas = numpy.array(dataframe[['CAS']],dtype=type('a'))
            names = numpy.array(dataframe[['Name']], dtype=type('a'))
            if measured is None:
                measured = ~numpy.isnan(responses)
            responses = responses[measured]
            cas = cas[measured]
            names = names[measured]
            ordict = {}
            ordict['responses'] = responses
            ordict['names'] = names
            ordict['cas'] = cas
            self.hallemresponses[OR] = ordict
        self.measured = measured

    def provide_compatible_data(self):
        """
        Create data structures compatible to previous csv-based implementation.
        """ 
        num_odors = sum(self.measured)
        num_recs =len(self.hallems)
        self.response = numpy.zeros((num_odors,num_recs),dtype=int)
        for rec_i,rec in enumerate(self.hallems):
            self.response[:,rec_i] = self.hallemresponses[rec]['responses']
        self.response = self.response.T
        self.odorant_list = self.hallemresponses[rec]['names']
        self.or_list = self.hallems


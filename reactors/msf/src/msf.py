import argparse
import sqlite3
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--files', help='Input MSF file(s) for parsing', required=True)
parser.add_argument('--output', help='Name of output CSV file', default='output.csv')

class ProteomeDiscovererMSF():

    def __init__(self, path_to_MSF):
        self.path = path_to_MSF
        self.con = sqlite3.connect(path_to_MSF)
        self.cur = self.con.cursor()
    
    def proteins(self, name_contains=None, sequence_contains=None, protein_id=None):
        query = """
                SELECT P.ProteinID, 
                       P.Sequence, 
                       PA.Description, 
                       PS.ProteinScore, 
                       PS.Coverage 
                FROM Proteins AS P 
                JOIN ProteinAnnotations AS PA ON P.ProteinID=PA.ProteinID
                JOIN ProteinScores as PS ON P.ProteinID=PS.ProteinID
                """
        if name_contains:
            query += 'WHERE PA.Description LIKE "%' + str(name_contains) + '%" '
        if sequence_contains:
            query += 'WHERE P.Sequence LIKE "%' + str(sequence_contains) + '%" '
        if protein_id:
            query += 'WHERE P.ProteinID=' + str(protein_id)
              
        proteins = []
        try:
            for item in self.cur.execute(query):
                proteins.append({
                             'protein_id': item[0],
                             'sequence': item[1],
                             'description': item[2],
                             'protein_score': item[3],
                             'coverage': item[4]
                            })
        except sqlite3.OperationalError:
            pass

        output = pd.DataFrame(proteins)
        return output


    def peptides(self, 
                 sequence=None, 
                 protein_id=None, 
                 protein_description=None, 
                 peptide_min_score=None, 
                 best=False, 
                 scan_number=None, 
                 confidence_level=None, 
                 search_engine_rank=None):
        query = """
                SELECT Pep.Sequence, 
                """
          
        if best:
            query += "    MAX(PepS.ScoreValue),"
        else:    
            query += "    PepS.ScoreValue,"
              
        query += """
                    PA.ProteinID,
                    PA.Description,
                    SH.ScanNumbers,
                    SH.Mass,
                    SH.Charge,
                    SH.RetentionTime
                FROM Peptides AS Pep
                JOIN PeptidesProteins AS PP ON Pep.PeptideID=PP.PeptideID
                JOIN PeptideScores AS PepS ON Pep.PeptideID=PepS.PeptideID
                JOIN ProteinAnnotations AS PA ON PP.ProteinID=PA.ProteinID
                JOIN SpectrumHeaders AS SH ON Pep.SpectrumID=SH.SpectrumID
                """
        wheres = []
        if sequence:
            wheres.append(' Pep.Sequence LIKE "%' + str(sequence) + '%" ')
        if protein_id:
            wheres.append(' PP.ProteinID=' + str(protein_id) + ' ')
        if protein_description:
            wheres.append(' PA.Description LIKE "%' + str(protein_description) + '%"')
        if peptide_min_score:
            wheres.append(' PepS.ScoreValue >= ' + str(peptide_min_score) + ' ')
        if scan_number:
            wheres.append(' SH.ScanNumbers =' + str(scan_number) + ' ')
        if confidence_level:
            wheres.append(' Pep.ConfidenceLevel >= ' + str(confidence_level) + ' ')
        if search_engine_rank:
            wheres.append(' Pep.SearchEngineRank <= ' + str(search_engine_rank) + ' ')
              
        if len(wheres) > 0:
            query += 'WHERE' + ' AND'.join(wheres)
            
        if best:
            query += """GROUP BY Pep.Sequence"""
          
        peptides = []       
        try:
            for item in self.cur.execute(query):
                peptides.append({
                               'sequence': item[0],
                               'score': item[1],
                               'protein_id': item[2],
                               'description': item[3],
                               'scan_number': item[4],
                               'mass': item[5],
                               'charge': item[6],
                               'scan_time': item[7]
                              })
        except sqlite3.OperationalError:
            pass

        output = pd.DataFrame(peptides)
        return output

def main(args):

    msf = ProteomeDiscovererMSF(args.files)
    df = msf.proteins()

    # TODO serialize dataframe?
    
    df.to_csv(args.output)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

from account.models import Lawyer,CASE

# fileinfo=filetags+" "+file_description
# def algorithm():
#     lawyer_dict={}
#     case_dict={}
#     for lawyer in Lawyer.objects.all():
#         cases=CASE.objects.filter(lawyer_id=lawyer.user_id,case_approval=True,is_running=False,is_rated=True,case_status="VICTORY")
#         for case in cases:
#                 case_dict[case.id]=case.file.filetags+" "+case.file.file_description
#         lawyer_dict[lawyer.user_id]=case_dict

#     lawyer_ids=[]
#     case_id=[]
#     for search in fileinfo.split():
#          for case_point in case_dict:
#             recommendations=get_recommendations(search, case_point)
#             for doc, similarity in recommendations:
#                  if similarity>0.5:
#                       case_id.append(doc)
#                       case = CASE.objects.get(id=doc)
#                       related_lawyers = case.lawyer.all()
#                       lawy_ids = [lawyer.user_id for lawyer in related_lawyers]
#                       lawyer_ids.append(lawy_ids)





# def main():
    #  algorithm()

# if __name__=="__main__":
#      main()
# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog

from swiplserver import PrologMQI




def find_door_solution(state):
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            result = prolog_thread.query("member(X, [first, second, third]).")

        with PrologMQI() as mqi_file:
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                result = prolog_thread.query("[knowledgebase].")
                print(result)

                string = str(state)
                query = 'action(' + string[1:-1] + ', Res).'

                print(query)

                result = prolog_thread.query(query)
                result_str = str(result)
                result_str = result_str[10:-3]

                print(result_str)

                return result_str



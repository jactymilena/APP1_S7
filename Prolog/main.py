# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog

from swiplserver import PrologMQI


if __name__ == '__main__':
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            result = prolog_thread.query("member(X, [first, second, third]).")
        #     print(result)

        with PrologMQI() as mqi_file:
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                result = prolog_thread.query("[knowledgebase].")
                print(result)

                result = prolog_thread.query("action(['silver','blue','red','white', '', ''], Res).")

                print(result)



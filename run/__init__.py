import matlab.engine
import matlab

INPUT_FLOW = ""
OUTPUT_FLOW = "results"

eng = matlab.engine.start_matlab()

def fuzzy_segment(fuzzy_system, *settings):
    edus = eng.run_and_get_edus(fuzzy_system, settings['training_data_path'])
    is_hilda = 'hilda' in settings and settings['hilda'] == True
    is_array = not is_hilda                 # Will default to true of hilda isn't present... 
                                            # TODO need a SPADE form? other RST parsers?
    return_string = "" if is_hilda else []  # default to array
    
    for segment in edus:
        if is_hilda:
            HILDA_form = f"<edu>{segment}</edu>\n"
            return_string += HILDA_form
        elif is_array:
            return_string.append(segment)

    return return_string


def start(input_data=None, settings={}, loop_breaker=None):
    print(f"RUNNING.... My input data is\n{input_data}")

    fuzzy_system = eng.train(settings['training_data_path'], False)
    
    edus = fuzzy_segment(fuzzy_system, *settings)

    if test_looper > 3:
        return 1, True
    else:
        test_looper += 1



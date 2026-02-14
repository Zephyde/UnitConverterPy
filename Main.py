from CalculationsUnits import extractAndReplaceMetricUnits, extractAndReplaceUnits, extractUnitsFromAnswer, extractUnitsFromText
import textwrap


while True:
    print("\nInput your paragraph here and end with an empty line: \n")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    if not lines:
        print("No input provided. Try again or Ctrl+C to exit.")
        continue

    textInput = "\n".join(lines)
    formatted_text = textwrap.fill(textInput, width=70)

    try:
        detected_units = extractUnitsFromText(textInput)
        if detected_units:
            print("\n🧪 Converted Text:")
            converted_text = extractAndReplaceUnits(textInput)
            formatted_converted = textwrap.fill(converted_text, width=70)
            print(formatted_converted)

            print("\nObi-Wan Unitobi says: 'Another happy conversion'")

            answer_input = input(
                "\nEnter your answer with the desired unit in metric for conversion to imperial, or enter 'quit': \n")

            if answer_input == "quit":
                break
            else:
                detected_metric_units = extractUnitsFromAnswer(answer_input)
                print(f"\n🧪 Detected Metric Units: {detected_metric_units}")
                for unit,values in detected_metric_units.items():
                    print (f"{unit}: {values}")

                if detected_metric_units:
                    imperial_answer = extractAndReplaceMetricUnits(answer_input)
                    print(imperial_answer)
                else:
                    print("No metric units detected in your answer.")

        else:
            print("Obi-Wan Unitobi says: 'I sense a great disturbance in your input units'")
            print("No units detected in your text, try again.")

    except ValueError as e:
        print(f"Error processing input: {e}")
        print("Please try again with valid input.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please try again.")
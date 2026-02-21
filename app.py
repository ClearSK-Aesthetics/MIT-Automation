import gradio as gr
from mit_parser import extract_text_from_scanned_pdf, parse_mit_fields
from mit_formatter import generate_mit_excel


def process_pdf(file):
    text = extract_text_from_scanned_pdf(file.name)
    parsed_data = parse_mit_fields(text)
    output_file = generate_mit_excel(parsed_data)

    return output_file


app = gr.Interface(
    fn=process_pdf,
    inputs=gr.File(label="Upload Scanned PDF"),
    outputs=gr.File(label="Download MIT Excel"),
    title="MIT Automation System",
    description="Upload scanned invoice PDF and auto-generate MIT formatted Excel"
)

if __name__ == "__main__":
    app.launch()

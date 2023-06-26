from modal import Image, Stub, gpu, method

BASE_MODEL = "openlm-research/open_llama_7b_400bt_preview"


def download_models():
    from transformers import LlamaForCausalLM, LlamaTokenizer

    LlamaForCausalLM.from_pretrained(BASE_MODEL)
    LlamaTokenizer.from_pretrained(BASE_MODEL)


image = (
    # Python 3.11+ not yet supported for torch.compile
    Image.debian_slim(python_version="3.10")
    .pip_install(
        "accelerate~=0.18.0",
        "transformers~=4.28.1",
        "torch~=2.0.0",
        "sentencepiece~=0.1.97",
    )
    .run_function(download_models)
)

stub = Stub(name="example-open-llama", image=image)


@stub.cls(gpu=gpu.A100(memory=20))
class OpenLlamaModel:
    def __enter__(self):
        import torch
        from transformers import LlamaForCausalLM, LlamaTokenizer

        self.tokenizer = LlamaTokenizer.from_pretrained(BASE_MODEL)

        model = LlamaForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        self.tokenizer.bos_token_id = 1

        model.eval()
        self.model = torch.compile(model)
        self.device = "cuda"

    @method()
    def generate(
        self,
        input,
        max_new_tokens=128,
        **kwargs,
    ):
        import torch
        from transformers import GenerationConfig

        inputs = self.tokenizer(input, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)

        generation_config = GenerationConfig(**kwargs)
        with torch.no_grad():
            generation_output = self.model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        output = self.tokenizer.decode(s)
        print(f"\033[96m{input}\033[0m")
        print(output.split(input)[1].strip())


@stub.local_entrypoint()
def main():
    inputs = [
        "LLM agents can be made comply with applicable laws by:",
    ]
    model = OpenLlamaModel()
    for input in inputs:
        model.generate.call(
            input,
            top_p=0.75,
            top_k=40,
            num_beams=1,
            temperature=0.1,
            do_sample=True,
        )

Your code:

```python
import torch
print(torch.get_device)
```

will **not** do what you expect.

Here’s why:
- `torch.get_device` **doesn't exist** directly like that in the PyTorch API.
- You probably meant to get the device of a **tensor**.

If you want to **check which device** a tensor is on, you should do something like:

```python
import torch

x = torch.tensor([1, 2, 3])  # This tensor will be on CPU by default
print(x.device)
```

Or if you want to **check if CUDA (GPU) is available**, and get the current device:

```python
print(torch.cuda.is_available())   # True if GPU is available
print(torch.cuda.current_device()) # Returns current GPU device ID (like 0)
print(torch.cuda.get_device_name(0))  # Get device name like "NVIDIA GeForce RTX 3060"
```

---
**Summary:**  
- `torch.get_device` — ❌ Not a valid function.  
- `tensor.device` — ✅ To get which device a tensor is on.
- `torch.cuda.current_device()` — ✅ To get current CUDA device ID.

---
Would you like me to show you a small script that prints whether PyTorch is using CPU or GPU dynamically? 🚀

# Customer Support Agents

## Hakkında

OpenAI Agents SDK'yı öğrenmek için yazdığım, terminalde çalışan küçük bir
müşteri destek botu. Gerçek bir ürün değil, bir öğrenme projesi: tüm tool'lar
sahte (mock) veri döndürüyor.

Amacım `Agent`, `Runner`, `function_tool`, `Agent.as_tool()` ve manager
(orchestrator) pattern'ini adım adım kurarak anlamaktı. Git geçmişi de bu
sırayı takip ediyor: önce tek bir agent, sonra function tool'lar, sonra uzman
agentlar ve en son manager.

Kullanılanlar:

- Python
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`openai-agents`)
- Groq'un OpenAI uyumlu API'si
- Model: `openai/gpt-oss-20b`

## Mimari

```text
                User
                 |
                 v
     Customer Support Manager  <---------------+
       |         |          |                  |
       v         v          v                  |
  technical_  billing_   general_              |
  support     support    support               |
  (agent as   (agent as  (agent as             |
   tool)       tool)      tool)                |
     |           |                             |
     v           v                             |
  function    function                         |
  tools       tools                            |
     |           |                             |
     +-----------+---- sonuç ------------------+
                 |
                 v
          Final cevap (manager yazar)
```

Bu projede handoff kullanılmıyor. Handoff'ta konuşmanın kontrolünü uzman agent
devralır. Burada ise manager, uzman agentı diğer tool'lar gibi çağırıyor,
cevabını string olarak geri alıyor ve kullanıcıya verilecek son cevabı her
zaman kendisi yazıyor.

## Agentlar

Tüm agentlar `support_agents.py` dosyasında tanımlı.

| Agent | Görevi | Tool'ları |
|---|---|---|
| Customer Support Manager | Uygun uzmanı seçer, son cevabı yazar | `technical_support`, `billing_support`, `general_support` |
| Technical Support Agent | Giriş sorunları, uygulama hataları, şifreler | `check_service_status`, `reset_password`, `create_technical_ticket` |
| Billing Support Agent | Ödemeler, abonelikler, faturalar | `get_subscription_info`, `cancel_subscription`, `create_billing_ticket` |
| General Support Agent | Şirket bilgisi, destek saatleri, iletişim | yok |

## Tool'lar

**Function tool'lar** (`tools.py`), `@function_tool` ile işaretlenmiş sıradan
Python fonksiyonları. SDK, type hint'lerden ve docstring'den bir JSON şeması
oluşturuyor. Model bu şemayı görüyor ve tool'u çağırıp çağırmayacağına, ne
zaman çağıracağına kendisi karar veriyor. Fonksiyonun kendisi ise lokalde,
Python içinde çalışıyor. Her tool, çalıştığı anı görebilmek için bir
`[tool] ...` satırı yazdırıyor.

**Agent as tool.** `agent.as_tool(tool_name=..., tool_description=...)`, bir
agentın tamamını tek bir `input` string parametresi alan bir tool'a çeviriyor.
Manager bu tool'u çağırdığında SDK, uzman agentı kendi agent loop'unda
çalıştırıyor ve onun `final_output` değerini tool sonucu olarak geri döndürüyor.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

https://console.groq.com/keys adresinden bir API anahtarı al, ardından
`.env.example` dosyasını `.env` olarak kopyalayıp anahtarı yaz:

```text
GROQ_API_KEY=your_key_here
```

Anahtar `python-dotenv` ile `.env` dosyasından yükleniyor ve `os.environ`
üzerinden okunuyor. `.env` dosyası `.gitignore` içinde. İstersen anahtarı
normal bir ortam değişkeni olarak da tanımlayabilirsin.

## Çalıştırma

```bash
python main.py
```

```text
Customer Support System (type 'exit' or 'quit' to leave)

You: Kartımdan iki kere ödeme alınmış.
  [tool] get_subscription_info()
  [tool] create_billing_ticket('Duplicate charge on 2026-09-15')
  [manager called billing_support]

Assistant: ...
```

Uzman agentın `[tool]` satırları `[manager called ...]` satırından önce
görünüyor. Bunun sebebi, manager'ın tool çağrılarının ancak tüm run
bittikten sonra yazdırılması.

Programı kapatmak için `exit` veya `quit` yaz.

## Neler öğrendim

- **Agent ile normal bir LLM çağrısı arasındaki fark.** Normal bir çağrı tek
  istek ve tek cevaptan oluşur. Agent ise model, talimatlar ve tool'ların bir
  döngü içinde çalışmasıdır: model bir tool isteyebilir, SDK o tool'u çalıştırıp
  sonucu modele geri gönderir ve bu, model son cevabı verene kadar tekrar eder.
- **Function tool'lar.** LLM hiçbir zaman kod çalıştırmaz. Yalnızca bir tool adı
  ve JSON argümanlar döndürür. Python fonksiyonunu `Runner` çağırır ve dönen
  değeri modele geri gönderir.
- **Agent as tool.** Uzman bir agent, tıpkı bir function tool gibi
  kullanılabilir. Manager açısından bu, string alıp string döndüren sıradan
  bir tool'dur.
- **Manager pattern.** Konuşmanın sahibi tek bir agenttır ve alt görevleri
  uzmanlara dağıtır. Handoff'a kıyasla tek bir üslup ve dil korumak, birden
  fazla uzmanın sonucunu birleştirmek daha kolaydır.
- **Agent loop.** `Runner.run()` bir döngü çalıştırır: modeli çağırır, istenen
  tool'ları çalıştırır, sonuçları girdiye ekler ve modeli tekrar çağırır. Model
  tool çağrısı içermeyen bir metin döndürdüğünde ya da `max_turns` sınırına
  ulaşıldığında durur.
- **Bir run'da birden fazla LLM çağrısı.** "Kartımdan iki kere ödeme alınmış"
  gibi tek bir mesaj yaklaşık 5 API çağrısına yol açabilir: manager billing'i
  çağırmaya karar verir, billing `get_subscription_info` ister, billing
  `create_billing_ticket` ister, billing özetini yazar ve manager son cevabı
  yazar.

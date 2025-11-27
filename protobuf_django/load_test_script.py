import httpx
from locust import User, task, between
from app.proto import data_pb2

USER_MESSAGE = data_pb2.Data(
    name="Roronoa Zoro",
    age=25,
    description='Roronoa Zoro is the combatant of the Straw Hat Pirates and one of the most iconic characters in One Piece. Physically imposing and incredibly muscular, Zoro stands tall with a powerful, broad-shouldered frame that reflects his years of relentless training and countless life-or-death battles. His appearance is instantly recognizable: short green hair, sharp eyes often narrowed in focus, and a stern expression that makes him look perpetually serious—even when he’s asleep or hopelessly lost. A defining part of his look is the black bandana tied around his left bicep, which he only wears on his head during the toughest battles, signaling that he’s fighting at full strength. Zoro wields three swords in a unique style known as Santoryu—the Three-Sword Style—where he holds one sword in each hand and a third in his mouth. His treasured blade is Wado Ichimonji, a white sword with deep personal significance tied to his childhood friend Kuina. Over the course of the series, he acquires other legendary swords such as the cursed Sandai Kitetsu, the black blade Shusui (later replaced with Enma), and his swordsmanship grows so powerful that entire buildings, ships, and mountains fall before his techniques. His body is a map of scars, each marking a brutal confrontation. The most famous is the massive X-shaped scar across his torso, inflicted by Mihawk during their first duel—a wound that represents both Zoro’s greatest defeat and the moment that hardened his resolve to surpass all limits. Another is the scar that runs over his left eye, earned during training with Mihawk during the two-year timeskip; though its origin is still mysterious, fans associate it with power he has yet to fully reveal. Personality-wise, Zoro is stern, disciplined, and unwavering in his convictions. He projects an aura of quiet intensity and rarely allows emotions to cloud his judgment. Though he is often blunt or harsh in his words, his loyalty to Luffy and the crew runs deeper than anything else. Zoro is the type who will throw himself in front of death without hesitation if it means protecting his captain’s dream. One of his most defining moments is when he takes on all of Luffy pain'
)

PROTO_DATA_BYTES = USER_MESSAGE.SerializeToString()

HEADERS_PROTOBUF = {
    'Content-Type': 'application/x-protobuf',
    'Accept': 'application/x-protobuf',
}

class ProtobufUser(User):
    wait_time = between(1, 2.5)
    host = "http://127.0.0.1:8000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # HTTP/2 client
        self.http2_client = httpx.Client(base_url=self.host, http2=True, timeout=10.0)

    @task
    def post_protobuf(self):
        name = "POST /api/data/ (Protobuf)"

        try:
            response = self.http2_client.post("/api/data/", content=PROTO_DATA_BYTES, headers=HEADERS_PROTOBUF)
            response_time_ms = response.elapsed.total_seconds() * 1000  # in milliseconds

            if response.status_code == 200:
                try:
                    response_message = data_pb2.Data()
                    response_message.ParseFromString(response.content)
                    print(response.content)
                    if response_message.name == "Roronoa Zoro" and response_message.age == 25:
                        # Fire Locust success event
                        self.environment.events.request.fire(
                            request_type="POST",
                            name=name,
                            response_time=response_time_ms,
                            response_length=len(response.content),
                            exception=None
                        )
                    else:
                        # Fire failure event
                        self.environment.events.request.fire(
                            request_type="POST",
                            name=name,
                            response_time=response_time_ms,
                            response_length=len(response.content),
                            exception=Exception(f"Protobuf Data Mismatch: Got {response_message.name}")
                        )
                except Exception as e:
                    # Fire failure event for parse errors
                    self.environment.events.request.fire(
                        request_type="POST",
                        name=name,
                        response_time=response_time_ms,
                        response_length=len(response.content),
                        exception=e
                    )
            else:
                # Fire failure event for bad HTTP status
                self.environment.events.request.fire(
                    request_type="POST",
                    name=name,
                    response_time=response_time_ms,
                    response_length=len(response.content),
                    exception=Exception(f"Status code {response.status_code}")
                )

        except Exception as e:
            # Fire failure event for connection errors
            self.environment.events.request.fire(
                request_type="POST",
                name=name,
                response_time=0,
                response_length=0,
                exception=e
            )

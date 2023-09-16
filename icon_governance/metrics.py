from prometheus_client import Counter, Gauge


class Metrics:
    def __init__(self):
        self.preps_created = Gauge(
            "preps_created",
            "Num created.",
        )
        self.preps_updated = Gauge("preps_updated", "Num updated.")

        self.preps_attributes_cron_ran = Counter(
            "preps_attributes_cron_ran",
            "Number times cron ran",
        )
        self.preps_proposals_cron_ran = Counter(
            "preps_proposals_cron_ran",
            "Number times cron ran",
        )
        self.preps_cps_cron_ran = Counter("preps_cps_cron_ran", "Number times cron ran")
        self.preps_base_cron_ran = Counter("preps_base_cron_ran", "Number times cron ran")
        self.preps_stake_cron_ran = Counter(
            "preps_stake_cron_ran",
            "Number times stake cron ran",
        )
        self.preps_state_cron_ran = Counter(
            "preps_state_cron_ran",
            "Number times state cron ran",
        )
        self.preps_iscore_cron_ran = Counter(
            "rewards_cron_ran",
            "Number times iscore cron ran",
        )
        self.preps_rewards_cron_ran = Counter(
            "preps_rewards_cron_ran",
            "Number of times rewards cron ran",
        )
        self.preps_public_key_cron_ran = Counter(
            "preps_public_key_cron_ran",
            "Number of times public key cron ran",
        )


prom_metrics = Metrics()

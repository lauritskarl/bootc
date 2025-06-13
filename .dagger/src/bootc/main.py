import dagger
from dagger import dag, function, object_type


@object_type
class Bootc:
    @function
    async def build_and_publish(self, registry: str, image_name: str, username: str, password: dagger.Secret) -> str:
        """Builds and publishes a Fedora bootc container with fish shell installed"""
        image_ref = f"{registry}/{image_name}"
        return await (
            dag.container()
            .from_("quay.io/fedora/fedora-bootc:latest")
            .with_exec(["dnf", "-y", "install", "fish"])
            .with_exec(["dnf", "clean", "all"])
            .with_registry_auth(
                address=registry,
                username=username,
                secret=password
            )
            .publish(image_ref)
        )

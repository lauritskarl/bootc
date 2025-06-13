import dagger
from dagger import dag, function, object_type


@object_type
class Bootc:
    @function
    async def build_and_publish(self, registry: str, image_name: str, tag: str, username: str, password: dagger.Secret) -> str:
        """Builds and publishes a Fedora bootc container with a specific tag"""
        # Construct the full image reference including the tag
        image_ref_with_tag = f"{registry}/{image_name}:{tag}"

        # Build the container
        built_container = (
            dag.container()
            .from_("quay.io/fedora/fedora-bootc:latest")
            .with_exec(["dnf", "-y", "install", "fish"])
            .with_exec(["dnf", "clean", "all"])
        )

        # Authenticate with the registry before publishing
        # The 'registry' parameter for with_registry_auth should be the server address, e.g., "ghcr.io"
        authed_container = built_container.with_registry_auth(
            address=registry,
            username=username,
            secret=password
        )

        # Publish the container with the specified tag and return the digest reference
        # The publish command returns a string like "ghcr.io/owner/image@sha256:thedigest"
        return await authed_container.publish(address=image_ref_with_tag).stdout()

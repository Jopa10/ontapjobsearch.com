"use client";

import { useEffect } from "react";

type DeploymentRefreshProps = {
  deploymentVersion: string | null;
};

export default function DeploymentRefresh({
  deploymentVersion,
}: DeploymentRefreshProps) {
  useEffect(() => {
    if (!deploymentVersion) return;

    let checking = false;

    async function checkForNewDeployment() {
      if (checking || document.visibilityState !== "visible") return;
      checking = true;

      try {
        const response = await fetch("/api/deployment-version", {
          cache: "no-store",
          headers: { "x-ontap-version-check": "1" },
        });
        if (!response.ok) return;

        const data = (await response.json()) as { version?: string | null };
        if (data.version && data.version !== deploymentVersion) {
          window.location.reload();
        }
      } catch {
        // A failed background version check should never interrupt the user.
      } finally {
        checking = false;
      }
    }

    function handleVisibilityChange() {
      if (document.visibilityState === "visible") {
        void checkForNewDeployment();
      }
    }

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("focus", checkForNewDeployment);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("focus", checkForNewDeployment);
    };
  }, [deploymentVersion]);

  return null;
}

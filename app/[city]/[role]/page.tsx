import { slices } from "../../../data/getSlice"

export default async function Page({
  params,
}: {
  params: Promise<{ city: string; role: string }>
}) {
  const { city, role } = await params

  const citySlug = decodeURIComponent(city).toLowerCase()
  const roleSlug = decodeURIComponent(role).toLowerCase()
  const key = `${citySlug}/${roleSlug}`

  const slice = (slices as Record<string, any>)[key]

  if (!slice) {
    return (
      <div style={{ padding: 40 }}>
        <div>
          <b>Not found</b>
        </div>
        <div>
          Looking for key: <code>{key}</code>
        </div>
        <div style={{ marginTop: 12 }}>
          Available keys (first 50):
          <pre>{Object.keys(slices).slice(0, 50).join("\n")}</pre>
        </div>
      </div>
    )
  }

  const job = slice.jobs?.[0]

  return (
    <main style={{ padding: 40 }}>
      <h1>
        {slice.role} jobs in {slice.city}
      </h1>

      {job ? (
        <>
          <h2>{job.title}</h2>
          <p>{job.company}</p>
          <p>{job.location}</p>
          <p>{job.salary}</p>
        </>
      ) : (
        <p>No jobs in this slice.</p>
      )}
    </main>
  )
}








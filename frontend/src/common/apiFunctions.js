export async function modifyPlacementDriveStatus(userRole, placementDriveId, action) {
  const actions = ['approve', 'decline', 'close', 'reopen'];
  if (!actions.includes(action)) {
    throw new Error(`Unsupported action specified: ${action}`);
  }

  const url = `/api/${userRole}/placement-drives/${placementDriveId}/${action}`;

  const response = await fetch(url, { method: 'POST', credentials: 'include' });
  const data = await response.json();
  if (!response.ok) throw Error(data.errors);

  const placementDrive = data.data.placement_drive;

  return placementDrive;
}
